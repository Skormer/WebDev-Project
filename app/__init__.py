from flask import Flask, redirect, url_for
from flask_login import current_user

from config import Config

from .extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes.auth import auth_bp
    from .routes.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)

    # Tabellen anlegen (nur neue; bestehende werden NICHT migriert -> siehe BUILD_PLAN.md).
    with app.app_context():
        from . import models  # noqa: F401  (Modelle registrieren)

        db.create_all()

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("profile.me"))
        return redirect(url_for("auth.login"))

    return app
