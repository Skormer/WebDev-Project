from flask import Flask, redirect, url_for
from flask_login import current_user
from sqlalchemy import inspect, text

from config import Config

from .extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes.auth import auth_bp
    from .routes.chat import chat_bp
    from .routes.listings import listings_bp
    from .routes.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(listings_bp)
    app.register_blueprint(profile_bp)

    # Tabellen anlegen (nur neue; bestehende werden NICHT migriert -> siehe BUILD_PLAN.md).
    with app.app_context():
        from . import models  # noqa: F401  (Modelle registrieren)

        db.create_all()
        _ensure_listing_geo_columns()
        _ensure_user_lifestyle_columns()

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("listings.index"))
        return redirect(url_for("auth.login"))

    @app.context_processor
    def inject_nav_counts():
        """Zähler für die Navigation (ungelesene Nachrichten + offene Inserat-Aktivität)."""
        if not current_user.is_authenticated:
            return {}
        from .models import Application, Appointment, Message

        unread = Message.query.filter_by(
            receiver_id=current_user.id, read_at=None
        ).count()
        activity = 0
        if current_user.listings:
            listing_id = current_user.listings[0].id
            activity = (
                Application.query.filter_by(listing_id=listing_id, status="offen").count()
                + Appointment.query.filter_by(listing_id=listing_id, status="offen").count()
            )
        return {"nav_unread_messages": unread, "nav_listing_activity": activity}

    return app


def _ensure_listing_geo_columns():
    """Add optional geo columns to older local SQLite DBs without a full migration setup."""
    inspector = inspect(db.engine)
    if "listing" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("listing")}
    with db.engine.begin() as connection:
        if "latitude" not in columns:
            connection.execute(text("ALTER TABLE listing ADD COLUMN latitude FLOAT"))
        if "longitude" not in columns:
            connection.execute(text("ALTER TABLE listing ADD COLUMN longitude FLOAT"))


def _ensure_user_lifestyle_columns():
    """Add optional profile lifestyle columns to older local DBs without migrations."""
    inspector = inspect(db.engine)
    if "user" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("user")}
    lifestyle_columns = {
        "hobbies": "TEXT",
        "musikgeschmack": "VARCHAR(200)",
        "wochenend_typ": "VARCHAR(30)",
        "soziales_level": "VARCHAR(30)",
        "kocht_gern": "BOOLEAN",
    }
    with db.engine.begin() as connection:
        for column_name, column_type in lifestyle_columns.items():
            if column_name not in columns:
                connection.execute(text(f"ALTER TABLE \"user\" ADD COLUMN {column_name} {column_type}"))
