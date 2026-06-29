from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    alter = db.Column(db.Integer)
    beruf = db.Column(db.String(120))
    budget_min = db.Column(db.Integer)
    budget_max = db.Column(db.Integer)
    raucher = db.Column(db.Boolean, default=False)
    haustiere = db.Column(db.Boolean, default=False)
    sauberkeit = db.Column(db.Integer)  # 1-5
    bio = db.Column(db.Text)
    foto_url = db.Column(db.String(500))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # "suchend" = sucht ein Zimmer/WG, "anbietend" = inseriert ein Zimmer/WG
    rolle = db.Column(db.String(20), nullable=False, default="suchend")

    listings = db.relationship("Listing", backref="owner", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class Listing(db.Model):
    __tablename__ = "listing"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rent = db.Column(db.Integer, nullable=False)
    deposit = db.Column(db.Integer)
    location = db.Column(db.String(200), nullable=False)
    room_size = db.Column(db.Integer)
    available_from = db.Column(db.Date)
    furnished = db.Column(db.Boolean, default=False)
    pets_allowed = db.Column(db.Boolean, default=False)
    smoking_allowed = db.Column(db.Boolean, default=False)
    flatmates = db.Column(db.Integer)
    photo_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Listing {self.title}>"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Weitere Tabellen (Listing, Message, ...) folgen in späteren Schritten – siehe BUILD_PLAN.md.
