import os
from uuid import uuid4

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, logout_user
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from ..extensions import db
from ..forms import ConfirmForm, ProfileEditForm
from ..models import Appointment, Application, Favorite, Listing, Message, User
from ..storage import upload_photo

profile_bp = Blueprint("profile", __name__)

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "uploads"))


@profile_bp.route("/profile")
@login_required
def me():
    return render_template("profile/view.html", user=current_user, own=True)


@profile_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit():
    form = ProfileEditForm(obj=current_user)
    if form.validate_on_submit():
        uploaded_file = form.foto.data
        if uploaded_file and uploaded_file.filename:
            filename_stem = uuid4().hex
            # Zuerst Supabase Storage (dauerhaft), sonst lokaler Fallback (nur Dev/ephemer).
            storage_url = upload_photo(uploaded_file, filename_stem, folder="profiles")
            if storage_url:
                current_user.foto_url = storage_url
            else:
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                original_name = secure_filename(uploaded_file.filename)
                _, extension = os.path.splitext(original_name)
                filename = f"{filename_stem}{extension.lower()}"
                uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))
                current_user.foto_url = url_for("static", filename=f"uploads/{filename}")
        elif form.foto_url.data:
            current_user.foto_url = form.foto_url.data.strip()

        current_user.name = form.name.data.strip()
        current_user.rolle = form.rolle.data
        current_user.alter = form.alter.data
        current_user.beruf = form.beruf.data.strip() if form.beruf.data else None
        current_user.stadt = form.stadt.data.strip() if form.stadt.data else None
        current_user.nationalitaet = form.nationalitaet.data.strip() if form.nationalitaet.data else None
        current_user.budget_min = form.budget_min.data
        current_user.budget_max = form.budget_max.data
        current_user.raucher = form.raucher.data
        current_user.haustiere = form.haustiere.data
        current_user.sauberkeit = form.sauberkeit.data
        current_user.hobbies = form.hobbies.data.strip() if form.hobbies.data else None
        current_user.musikgeschmack = form.musikgeschmack.data.strip() if form.musikgeschmack.data else None
        current_user.wochenend_typ = form.wochenend_typ.data or None
        current_user.soziales_level = form.soziales_level.data or None
        current_user.bio = form.bio.data.strip() if form.bio.data else None
        db.session.commit()
        flash("Profil gespeichert.", "success")
        return redirect(url_for("profile.me"))

    return render_template("profile/edit.html", form=form, user=current_user, delete_form=ConfirmForm())


@profile_bp.route("/profile/delete", methods=["POST"])
@login_required
def delete():
    form = ConfirmForm()
    if not form.validate_on_submit():
        flash("Profil konnte nicht gelöscht werden.", "warning")
        return redirect(url_for("profile.edit"))

    user_id = current_user.id
    user_name = current_user.name
    listing_ids = [listing.id for listing in current_user.listings]

    if listing_ids:
        Favorite.query.filter(Favorite.listing_id.in_(listing_ids)).delete(synchronize_session=False)
        Application.query.filter(Application.listing_id.in_(listing_ids)).delete(synchronize_session=False)
        Appointment.query.filter(Appointment.listing_id.in_(listing_ids)).delete(synchronize_session=False)
        Message.query.filter(Message.listing_id.in_(listing_ids)).delete(synchronize_session=False)
        for listing in list(current_user.listings):
            db.session.delete(listing)

    Favorite.query.filter_by(user_id=user_id).delete(synchronize_session=False)
    Application.query.filter_by(applicant_id=user_id).delete(synchronize_session=False)
    Appointment.query.filter(
        or_(Appointment.applicant_id == user_id, Appointment.owner_id == user_id)
    ).delete(synchronize_session=False)
    Message.query.filter(
        or_(Message.sender_id == user_id, Message.receiver_id == user_id)
    ).delete(synchronize_session=False)

    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    flash(f"Dein Profil wurde gelöscht, {user_name}.", "success")
    return redirect(url_for("auth.login"))


@profile_bp.route("/profile/<int:user_id>")
@login_required
def view(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("profile/view.html", user=user, own=(user.id == current_user.id))
