import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


def _normalize_db_url(url):
    """Supabase/Heroku hand out ``postgres://`` URLs; SQLAlchemy needs ``postgresql://``."""
    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")
    SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
    SUPABASE_STORAGE_KEY = os.environ.get("SUPABASE_STORAGE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    SUPABASE_STORAGE_BUCKET = os.environ.get("SUPABASE_STORAGE_BUCKET", "images")

    # Ohne DATABASE_URL: lokale SQLite-Datei; mit: Supabase/Postgres.
    SQLALCHEMY_DATABASE_URI = _normalize_db_url(os.environ.get("DATABASE_URL")) or (
        "sqlite:///" + os.path.join(basedir, "flatmate.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # pre_ping: reconnect nach inaktiven/gedroppten Supabase-Verbindungen.
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # E-Mail via SendGrid; ohne Key/Absender werden Mails nur geloggt.
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    MAIL_FROM = os.environ.get("MAIL_FROM")  # die in SendGrid verifizierte Absender-Adresse
    MAIL_FROM_NAME = os.environ.get("MAIL_FROM_NAME", "FlatMate")
