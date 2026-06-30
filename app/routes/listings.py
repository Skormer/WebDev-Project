import os
from datetime import date
from uuid import uuid4

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from ..email import send_email
from ..extensions import db
from ..forms import ApplicationForm, AppointmentForm, ConfirmForm, ListingForm
from ..models import Application, Appointment, Favorite, Listing

listings_bp = Blueprint("listings", __name__, url_prefix="/listings")

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "uploads", "listings"))


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


@listings_bp.route("/")
@login_required
def index():
    filters = {
        "kanton": request.args.get("kanton", "").strip(),
        "ort": request.args.get("ort", "").strip(),
        "rent_max": request.args.get("rent_max", "").strip(),
        "room_size_min": request.args.get("room_size_min", "").strip(),
        "available_by": request.args.get("available_by", "").strip(),
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

    if filters["kanton"]:
        query = query.filter(Listing.kanton == filters["kanton"])

    if filters["ort"]:
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
    active_filters = any(
        value for key, value in filters.items()
        if not (key == "rent_max" and value == "3000")
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
        photo_url = None
        uploaded_file = form.foto.data
        if uploaded_file and uploaded_file.filename:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            original_name = secure_filename(uploaded_file.filename)
            _, extension = os.path.splitext(original_name)
            filename = f"{uuid4().hex}{extension.lower()}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_file.save(file_path)
            photo_url = url_for("static", filename=f"uploads/listings/{filename}")

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
            photo_url=photo_url,
        )
        db.session.add(listing)
        db.session.commit()
        flash("Inserat erstellt.", "success")
        return redirect(url_for("listings.detail", listing_id=listing.id))

    return render_template("listings/new.html", form=form)


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
