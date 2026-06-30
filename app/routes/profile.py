import os
from uuid import uuid4

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from ..extensions import db
from ..forms import ProfileEditForm
from ..models import User

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
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            original_name = secure_filename(uploaded_file.filename)
            _, extension = os.path.splitext(original_name)
            filename = f"{uuid4().hex}{extension.lower()}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_file.save(file_path)
            current_user.foto_url = url_for("static", filename=f"uploads/{filename}")

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
        current_user.bio = form.bio.data.strip() if form.bio.data else None
        db.session.commit()
        flash("Profil gespeichert.", "success")
        return redirect(url_for("profile.me"))

    return render_template("profile/edit.html", form=form, user=current_user)


@profile_bp.route("/profile/<int:user_id>")
@login_required
def view(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("profile/view.html", user=user, own=(user.id == current_user.id))
