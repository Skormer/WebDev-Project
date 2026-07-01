import os
import json
import math
from datetime import date
from urllib.parse import urlencode
from urllib.request import urlopen
from uuid import uuid4

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from ..email import send_email
from ..extensions import db
from ..forms import ApplicationForm, AppointmentForm, ConfirmForm, ListingForm
from ..models import Application, Appointment, Favorite, Listing
from ..storage import upload_listing_photo

listings_bp = Blueprint("listings", __name__, url_prefix="/listings")

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "uploads", "listings"))

FALLBACK_GEO_POINTS = {
    "zurich": (47.3769, 8.5417),
    "zuerich": (47.3769, 8.5417),
    "zürich": (47.3769, 8.5417),
    "basel": (47.5596, 7.5886),
    "bern": (46.9480, 7.4474),
    "winterthur": (47.4988, 8.7237),
}


def _parse_int(value):
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _parse_date(value):
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _listing_address(listing):
    return ", ".join(
        part
        for part in [listing.strasse, listing.ort, listing.kanton, "Switzerland"]
        if part
    )


def _fallback_geocode(address):
    normalized = address.strip().lower()
    for key, coords in FALLBACK_GEO_POINTS.items():
        if key in normalized:
            return coords
    return None


def _geocode_address(address):
    if not address:
        return None

    api_key = current_app.config.get("GOOGLE_MAPS_API_KEY")
    if api_key:
        params = urlencode({"address": address, "key": api_key})
        try:
            with urlopen(f"https://maps.googleapis.com/maps/api/geocode/json?{params}", timeout=5) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception:
            payload = None

        if payload and payload.get("status") == "OK" and payload.get("results"):
            location = payload["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]

    return _fallback_geocode(address)


def _assign_listing_coordinates(listing):
    coords = _geocode_address(_listing_address(listing))
    if coords:
        listing.latitude, listing.longitude = coords
        return True
    listing.latitude = None
    listing.longitude = None
    return False


def _distance_km(origin, listing):
    if listing.latitude is None or listing.longitude is None:
        return None

    lat1, lon1 = origin
    lat2, lon2 = listing.latitude, listing.longitude
    radius = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    return radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _save_listing_photo(uploaded_file):
    """Speichert ein hochgeladenes JPEG und gibt dessen statische URL zurück (sonst None)."""
    if uploaded_file and uploaded_file.filename:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        original_name = secure_filename(uploaded_file.filename)
        _, extension = os.path.splitext(original_name)
        filename_stem = uuid4().hex
        storage_url = upload_listing_photo(uploaded_file, filename_stem)
        if storage_url:
            return storage_url

        filename = f"{filename_stem}{extension.lower()}"
        uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))
        return url_for("static", filename=f"uploads/listings/{filename}")
    return None


@listings_bp.route("/")
@login_required
def index():
    filters = {
        "kanton": request.args.get("kanton", "").strip(),
        "ort": request.args.get("ort", "").strip(),
        "rent_max": request.args.get("rent_max", "").strip(),
        "room_size_min": request.args.get("room_size_min", "").strip(),
        "available_by": request.args.get("available_by", "").strip(),
        "near": request.args.get("near", "").strip(),
        "radius_km": request.args.get("radius_km", "").strip(),
        "furnished": request.args.get("furnished", "").strip(),
        "pets_allowed": request.args.get("pets_allowed", "").strip(),
        "smoking_allowed": request.args.get("smoking_allowed", "").strip(),
    }

    available_kantons = [
        row[0]
        for row in (
            db.session.query(Listing.kanton)
            .filter(Listing.kanton.isnot(None), Listing.kanton != "")
            .distinct()
            .order_by(Listing.kanton.asc())
            .all()
        )
    ]

    query = Listing.query
    radius_km = _parse_int(filters["radius_km"])
    radius_origin_text = filters["near"] or filters["ort"]
    use_radius_search = bool(radius_origin_text)

    if filters["kanton"]:
        query = query.filter(Listing.kanton == filters["kanton"])

    if filters["ort"] and not use_radius_search:
        query = query.filter(Listing.ort.ilike(f"%{filters['ort']}%"))

    rent_max = _parse_int(filters["rent_max"])
    if rent_max is not None and rent_max < 3000:
        query = query.filter(Listing.rent <= rent_max)

    room_size_min = _parse_int(filters["room_size_min"])
    if room_size_min is not None:
        query = query.filter(Listing.room_size >= room_size_min)

    available_by = _parse_date(filters["available_by"])
    if available_by is not None:
        query = query.filter(Listing.available_from <= available_by)

    if filters["furnished"] == "yes":
        query = query.filter(Listing.furnished.is_(True))

    if filters["pets_allowed"] == "yes":
        query = query.filter(Listing.pets_allowed.is_(True))

    if filters["smoking_allowed"] == "yes":
        query = query.filter(Listing.smoking_allowed.is_(True))

    listings = query.order_by(Listing.created_at.desc()).all()

    if use_radius_search:
        radius_km = radius_km or 100
        origin = _geocode_address(radius_origin_text)
        if origin:
            listings_with_distance = []
            coordinates_updated = False
            for listing in listings:
                if listing.latitude is None or listing.longitude is None:
                    _assign_listing_coordinates(listing)
                    coordinates_updated = listing.latitude is not None and listing.longitude is not None or coordinates_updated
                distance = _distance_km(origin, listing)
                if distance is not None and (radius_km >= 100 or distance <= radius_km):
                    listings_with_distance.append((distance, listing))
            if coordinates_updated:
                db.session.commit()
            listings = [listing for _, listing in sorted(listings_with_distance, key=lambda item: item[0])]
        else:
            flash("Ort fuer Umkreissuche konnte nicht gefunden werden.", "warning")

    active_filters = any(
        value
        for key, value in filters.items()
        if not (
            (key == "rent_max" and value == "3000")
            or key == "radius_km"
        )
    )
    return render_template(
        "listings/index.html",
        listings=listings,
        filters=filters,
        available_kantons=available_kantons,
        active_filters=active_filters,
    )


@listings_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    # Pro User nur ein Inserat (siehe BUILD_PLAN.md).
    if current_user.listings:
        flash("Du hast bereits ein Inserat – pro Person ist nur eines möglich.", "info")
        return redirect(url_for("listings.detail", listing_id=current_user.listings[0].id))

    form = ListingForm()
    if form.validate_on_submit():
        listing = Listing(
            owner=current_user,
            title=form.title.data.strip(),
            description=form.description.data.strip(),
            rent=form.rent.data,
            deposit=form.deposit.data,
            kanton=form.kanton.data.strip(),
            ort=form.ort.data.strip(),
            strasse=form.strasse.data.strip() if form.strasse.data else None,
            room_size=form.room_size.data,
            available_from=form.available_from.data,
            furnished=form.furnished.data,
            pets_allowed=form.pets_allowed.data,
            smoking_allowed=form.smoking_allowed.data,
            flatmates=form.flatmates.data,
            photo_url=_save_listing_photo(form.foto.data),
        )
        coordinates_found = _assign_listing_coordinates(listing)
        db.session.add(listing)
        # Wer ein Inserat anbietet, ist nicht mehr "Auf Wohnungssuche".
        current_user.rolle = "anbietend"
        db.session.commit()
        flash("Inserat erstellt.", "success")
        if not coordinates_found:
            flash("Adresse konnte nicht eindeutig auf der Karte gefunden werden. Bitte Strasse, Hausnummer, Ort und Kanton pruefen.", "warning")
        return redirect(url_for("listings.detail", listing_id=listing.id))

    return render_template("listings/form.html", form=form, heading="Inserat erstellen")


@listings_bp.route("/<int:listing_id>/edit", methods=["GET", "POST"])
@login_required
def edit(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.owner_id != current_user.id:
        abort(403)

    form = ListingForm(obj=listing)
    if form.validate_on_submit():
        listing.title = form.title.data.strip()
        listing.description = form.description.data.strip()
        listing.rent = form.rent.data
        listing.deposit = form.deposit.data
        listing.kanton = form.kanton.data.strip()
        listing.ort = form.ort.data.strip()
        listing.strasse = form.strasse.data.strip() if form.strasse.data else None
        listing.room_size = form.room_size.data
        listing.available_from = form.available_from.data
        listing.furnished = form.furnished.data
        listing.pets_allowed = form.pets_allowed.data
        listing.smoking_allowed = form.smoking_allowed.data
        listing.flatmates = form.flatmates.data
        coordinates_found = _assign_listing_coordinates(listing)
        new_photo = _save_listing_photo(form.foto.data)
        if new_photo:
            listing.photo_url = new_photo
        db.session.commit()
        flash("Inserat aktualisiert.", "success")
        if not coordinates_found:
            flash("Adresse konnte nicht eindeutig auf der Karte gefunden werden. Bitte Strasse, Hausnummer, Ort und Kanton pruefen.", "warning")
        return redirect(url_for("listings.detail", listing_id=listing.id))

    return render_template("listings/form.html", form=form, heading="Inserat bearbeiten", listing=listing)


@listings_bp.route("/favorites")
@login_required
def favorites():
    favorites = (
        Favorite.query.filter_by(user_id=current_user.id)
        .order_by(Favorite.created_at.desc())
        .all()
    )
    return render_template(
        "listings/favorites.html",
        favorites=favorites,
        favorite_form=ConfirmForm(),
    )


@listings_bp.route("/map")
@login_required
def map_view():
    listings = Listing.query.order_by(Listing.created_at.desc()).all()
    map_listings = [
        {
            "title": listing.title,
            "description": listing.description,
            "rent": listing.rent,
            "deposit": listing.deposit,
            "room_size": listing.room_size,
            "available_from": listing.available_from.strftime("%d.%m.%Y") if listing.available_from else None,
            "furnished": listing.furnished,
            "pets_allowed": listing.pets_allowed,
            "smoking_allowed": listing.smoking_allowed,
            "photo_url": listing.photo_url,
            "latitude": listing.latitude,
            "longitude": listing.longitude,
            "address": _listing_address(listing),
            "detail_url": url_for("listings.detail", listing_id=listing.id),
        }
        for listing in listings
    ]
    return render_template(
        "listings/map.html",
        listings=listings,
        map_listings=map_listings,
    )


@listings_bp.route("/<int:listing_id>")
@login_required
def detail(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    is_owner = listing.owner_id == current_user.id

    application_count = 0
    appointment_count = 0
    my_application = None
    my_appointments = []
    is_favorite = False
    if is_owner:
        # Nur offene (nicht abgelehnte) Bewerbungen zählen.
        application_count = Application.query.filter(
            Application.listing_id == listing.id, Application.status != "abgelehnt"
        ).count()
        appointment_count = Appointment.query.filter_by(
            listing_id=listing.id, status="offen"
        ).count()
    else:
        my_application = Application.query.filter_by(
            listing_id=listing.id, applicant_id=current_user.id
        ).first()
        my_appointments = (
            Appointment.query.filter_by(listing_id=listing.id, applicant_id=current_user.id)
            .order_by(Appointment.scheduled_at.desc())
            .all()
        )
        is_favorite = Favorite.query.filter_by(
            user_id=current_user.id, listing_id=listing.id
        ).first() is not None

    return render_template(
        "listings/detail.html",
        listing=listing,
        owner=listing.owner,
        is_owner=is_owner,
        application_count=application_count,
        appointment_count=appointment_count,
        my_application=my_application,
        my_appointments=my_appointments,
        is_favorite=is_favorite,
        form=ApplicationForm(),
        favorite_form=ConfirmForm(),
        appointment_form=AppointmentForm(),
    )


@listings_bp.route("/<int:listing_id>/favorite", methods=["POST"])
@login_required
def toggle_favorite(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.owner_id == current_user.id:
        flash("Du kannst dein eigenes Inserat nicht favorisieren.", "info")
        return redirect(url_for("listings.detail", listing_id=listing.id))

    form = ConfirmForm()
    if form.validate_on_submit():
        favorite = Favorite.query.filter_by(
            user_id=current_user.id, listing_id=listing.id
        ).first()
        if favorite:
            db.session.delete(favorite)
            flash("Aus Favoriten entfernt.", "info")
        else:
            db.session.add(Favorite(user_id=current_user.id, listing_id=listing.id))
            flash("Zu Favoriten hinzugefuegt.", "success")
        db.session.commit()

    next_url = request.form.get("next") or url_for("listings.detail", listing_id=listing.id)
    return redirect(next_url)


@listings_bp.route("/<int:listing_id>/appointments")
@login_required
def appointments(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.owner_id != current_user.id:
        abort(403)

    all_appointments = (
        Appointment.query.filter_by(listing_id=listing.id)
        .order_by(Appointment.scheduled_at.asc(), Appointment.created_at.desc())
        .all()
    )
    open_appointments = [a for a in all_appointments if a.status == "offen"]
    handled_appointments = [a for a in all_appointments if a.status != "offen"]

    return render_template(
        "listings/appointments.html",
        listing=listing,
        open_appointments=open_appointments,
        handled_appointments=handled_appointments,
        confirm_form=ConfirmForm(),
    )


@listings_bp.route("/<int:listing_id>/appointments/request", methods=["POST"])
@login_required
def request_appointment(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.owner_id == current_user.id:
        flash("Du kannst fuer dein eigenes Inserat keinen Besichtigungstermin anfragen.", "warning")
        return redirect(url_for("listings.detail", listing_id=listing.id))

    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(
            listing_id=listing.id,
            applicant_id=current_user.id,
            owner_id=listing.owner_id,
            scheduled_at=form.scheduled_at.data,
            nachricht=form.nachricht.data.strip() if form.nachricht.data else None,
            status="offen",
        )
        db.session.add(appointment)
        db.session.commit()

        # Inserent per E-Mail über die Besichtigungsanfrage informieren (Fehler bricht nichts ab).
        appointments_url = url_for("listings.appointments", listing_id=listing.id, _external=True)
        html = render_template(
            "email/appointment_notification.html",
            owner_name=listing.owner.name,
            applicant_name=current_user.name,
            listing_title=listing.title,
            scheduled_at=appointment.scheduled_at,
            applicant_message=appointment.nachricht,
            appointments_url=appointments_url,
        )
        text = (
            f"Hallo {listing.owner.name},\n\n"
            f"{current_user.name} möchte dein Inserat „{listing.title}“ besichtigen.\n"
            f"Wunschtermin: {appointment.scheduled_at.strftime('%d.%m.%Y %H:%M')} Uhr\n"
            + (f"\nNachricht: {appointment.nachricht}\n" if appointment.nachricht else "")
            + f"\nBesichtigungen verwalten: {appointments_url}\n"
        )
        send_email(
            to=listing.owner.email,
            subject=f"Neue Besichtigungsanfrage für „{listing.title}“",
            html=html,
            text=text,
        )
        flash("Besichtigungsanfrage gesendet.", "success")
    else:
        flash("Bitte Datum und Uhrzeit fuer die Besichtigung auswaehlen.", "warning")

    return redirect(url_for("listings.detail", listing_id=listing.id))


@listings_bp.route("/<int:listing_id>/appointments/<int:appointment_id>/<decision>", methods=["POST"])
@login_required
def decide_appointment(listing_id, appointment_id, decision):
    listing = Listing.query.get_or_404(listing_id)
    if listing.owner_id != current_user.id:
        abort(403)
    if decision not in {"accept", "reject"}:
        abort(404)

    appointment = Appointment.query.filter_by(
        id=appointment_id, listing_id=listing.id
    ).first_or_404()

    if ConfirmForm().validate_on_submit():
        appointment.status = "angenommen" if decision == "accept" else "abgelehnt"
        db.session.commit()
        flash("Besichtigungstermin aktualisiert.", "success")

    return redirect(url_for("listings.appointments", listing_id=listing.id))


@listings_bp.route("/<int:listing_id>/applications")
@login_required
def applications(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.owner_id != current_user.id:
        abort(403)

    all_apps = (
        Application.query.filter_by(listing_id=listing.id)
        .order_by(Application.created_at.desc())
        .all()
    )
    open_apps = [a for a in all_apps if a.status != "abgelehnt"]
    rejected_apps = [a for a in all_apps if a.status == "abgelehnt"]

    return render_template(
        "listings/applications.html",
        listing=listing,
        open_apps=open_apps,
        rejected_apps=rejected_apps,
        reject_form=ConfirmForm(),
    )


@listings_bp.route("/<int:listing_id>/applications/<int:application_id>/reject", methods=["POST"])
@login_required
def reject_application(listing_id, application_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.owner_id != current_user.id:
        abort(403)

    application = Application.query.filter_by(
        id=application_id, listing_id=listing.id
    ).first_or_404()

    if ConfirmForm().validate_on_submit():
        application.status = "abgelehnt"
        db.session.commit()
        flash(f"Bewerbung von {application.applicant.name} abgelehnt.", "info")

    return redirect(url_for("listings.applications", listing_id=listing.id))


@listings_bp.route("/<int:listing_id>/apply", methods=["POST"])
@login_required
def apply(listing_id):
    listing = Listing.query.get_or_404(listing_id)

    if listing.owner_id == current_user.id:
        flash("Du kannst dich nicht auf dein eigenes Inserat bewerben.", "warning")
        return redirect(url_for("listings.detail", listing_id=listing.id))

    if Application.query.filter_by(listing_id=listing.id, applicant_id=current_user.id).first():
        flash("Du hast dich bereits auf dieses Inserat beworben.", "info")
        return redirect(url_for("listings.detail", listing_id=listing.id))

    form = ApplicationForm()
    if form.validate_on_submit():
        application = Application(
            listing_id=listing.id,
            applicant_id=current_user.id,
            nachricht=form.nachricht.data.strip() if form.nachricht.data else None,
            status="offen",
        )
        db.session.add(application)
        db.session.commit()

        # Inserent per E-Mail benachrichtigen (schlägt der Versand fehl, bleibt die Bewerbung trotzdem).
        applications_url = url_for("listings.applications", listing_id=listing.id, _external=True)
        html = render_template(
            "email/application_notification.html",
            owner_name=listing.owner.name,
            applicant_name=current_user.name,
            listing_title=listing.title,
            applicant_message=application.nachricht,
            applications_url=applications_url,
        )
        text = (
            f"Hallo {listing.owner.name},\n\n"
            f"{current_user.name} hat sich auf dein Inserat „{listing.title}“ beworben.\n"
            + (f"\nNachricht: {application.nachricht}\n" if application.nachricht else "")
            + f"\nBewerbungen ansehen: {applications_url}\n"
        )
        send_email(
            to=listing.owner.email,
            subject=f"Neue Bewerbung für „{listing.title}“",
            html=html,
            text=text,
        )
        flash("Bewerbung gesendet.", "success")

    return redirect(url_for("listings.detail", listing_id=listing.id))
