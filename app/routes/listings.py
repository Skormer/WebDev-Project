import os
from datetime import date
from uuid import uuid4

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from ..extensions import db
from ..forms import ListingForm
from ..models import Listing

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
        "pets_allowed": request.args.get("pets_allowed", "").strip(),
        "smoking_allowed": request.args.get("smoking_allowed", "").strip(),
    }

    query = Listing.query

    if filters["kanton"]:
        query = query.filter(Listing.kanton.ilike(f"%{filters['kanton']}%"))

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
        active_filters=active_filters,
    )


@listings_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
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


@listings_bp.route("/<int:listing_id>")
@login_required
def detail(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return render_template("listings/detail.html", listing=listing, owner=listing.owner)
