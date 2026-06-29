from flask import Blueprint, render_template
from flask_login import current_user, login_required

from ..models import Listing

listings_bp = Blueprint("listings", __name__, url_prefix="/listings")


@listings_bp.route("/")
@login_required
def index():
    listings = Listing.query.order_by(Listing.created_at.desc()).all()
    return render_template("listings/index.html", listings=listings)


@listings_bp.route("/<int:listing_id>")
@login_required
def detail(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return render_template("listings/detail.html", listing=listing, owner=listing.owner)
