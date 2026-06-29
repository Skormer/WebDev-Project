import os
from uuid import uuid4

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from ..extensions import db
from ..forms import ListingForm
from ..models import Listing

listings_bp = Blueprint("listings", __name__, url_prefix="/listings")

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "uploads", "listings"))


@listings_bp.route("/")
@login_required
def index():
    listings = Listing.query.order_by(Listing.created_at.desc()).all()
    return render_template("listings/index.html", listings=listings)


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
            location=form.location.data.strip(),
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
