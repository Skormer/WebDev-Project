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

    # Falls keine DATABASE_URL gesetzt ist -> lokale SQLite-Datei (läuft sofort ohne Setup).
    # Für Supabase/Postgres einfach DATABASE_URL in .env eintragen.
    SQLALCHEMY_DATABASE_URI = _normalize_db_url(os.environ.get("DATABASE_URL")) or (
        "sqlite:///" + os.path.join(basedir, "flatemate.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # E-Mail (SendGrid HTTP-API, Single Sender Verification — keine eigene Domain nötig).
    # Ohne SENDGRID_API_KEY oder MAIL_FROM werden Mails nur ins Log geschrieben
    # (lokale Entwicklung) statt wirklich versendet.
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    MAIL_FROM = os.environ.get("MAIL_FROM")  # die in SendGrid verifizierte Absender-Adresse
    MAIL_FROM_NAME = os.environ.get("MAIL_FROM_NAME", "FlateMate")
