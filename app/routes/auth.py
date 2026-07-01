from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..email import send_email
from ..extensions import db
from ..forms import LoginForm, RegisterForm
from ..models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("listings.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("listings.index"))
        flash("Email oder Passwort falsch.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("profile.me"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if User.query.filter_by(email=email).first():
            flash("Diese Email ist bereits registriert.", "warning")
        else:
            user = User(name=form.name.data.strip(), email=email)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            profile_url = url_for("profile.me", _external=True)
            html = render_template(
                "email/welcome.html",
                user_name=user.name,
                profile_url=profile_url,
            )
            text = (
                f"Hallo {user.name},\n\n"
                "willkommen bei FlatMate. Dein Konto wurde erfolgreich erstellt.\n"
                f"\nProfil vervollständigen: {profile_url}\n"
            )
            send_email(
                to=user.email,
                subject="Willkommen bei FlatMate",
                html=html,
                text=text,
            )
            login_user(user)
            flash("Konto erstellt – willkommen bei FlatMate!", "success")
            return redirect(url_for("profile.me"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Du bist ausgeloggt.", "info")
    return redirect(url_for("auth.login"))
