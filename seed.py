"""Legt die Tabellen neu an und füllt 10 Dummy-User plus Dummy-Inserate ein.

    python seed.py

ACHTUNG: drop_all() löscht bestehende Daten. Login zum Testen:
    lena@example.com / test1234   (Passwort ist bei allen gleich)
"""

from datetime import date

from app import create_app
from app.extensions import db
from app.models import Listing, User

app = create_app()

DUMMY_USERS = [
    {"name": "Lena Meier", "email": "lena@example.com", "alter": 24, "beruf": "Studentin",
     "budget_min": 600, "budget_max": 900, "raucher": False, "haustiere": False, "sauberkeit": 4,
     "bio": "Suche eine WG in Zürich, mag Kochen und Klettern."},
    {"name": "Tim Brunner", "email": "tim@example.com", "alter": 28, "beruf": "Software Engineer",
     "budget_min": 800, "budget_max": 1200, "raucher": False, "haustiere": True, "sauberkeit": 3,
     "bio": "Ruhiger Mitbewohner mit Katze, arbeite oft im Homeoffice."},
    {"name": "Sara Keller", "email": "sara@example.com", "alter": 31, "beruf": "Lehrerin",
     "budget_min": 700, "budget_max": 1000, "raucher": False, "haustiere": False, "sauberkeit": 5,
     "bio": "Ordnungsliebend, gerne gemeinsame Abendessen."},
    {"name": "Marco Rossi", "email": "marco@example.com", "alter": 26, "beruf": "Grafiker",
     "budget_min": 500, "budget_max": 800, "raucher": True, "haustiere": False, "sauberkeit": 2,
     "bio": "Kreativ, Nachtmensch, spiele Gitarre."},
    {"name": "Nina Huber", "email": "nina@example.com", "alter": 23, "beruf": "Studentin",
     "budget_min": 550, "budget_max": 850, "raucher": False, "haustiere": False, "sauberkeit": 4,
     "bio": "Sportlich, suche eine unkomplizierte WG nahe der Uni."},
    {"name": "David Frei", "email": "david@example.com", "alter": 35, "beruf": "Architekt",
     "budget_min": 1000, "budget_max": 1500, "raucher": False, "haustiere": False, "sauberkeit": 4,
     "bio": "Reise viel, brauche vor allem einen guten Schlafplatz."},
    {"name": "Elif Yilmaz", "email": "elif@example.com", "alter": 29, "beruf": "Krankenpflegerin",
     "budget_min": 700, "budget_max": 1100, "raucher": False, "haustiere": True, "sauberkeit": 3,
     "bio": "Schichtarbeit, daher manchmal tagsüber zuhause. Habe einen Hund."},
    {"name": "Jonas Weber", "email": "jonas@example.com", "alter": 27, "beruf": "Doktorand",
     "budget_min": 600, "budget_max": 950, "raucher": False, "haustiere": False, "sauberkeit": 3,
     "bio": "Lese gerne, koche viel vegetarisch."},
    {"name": "Aline Roth", "email": "aline@example.com", "alter": 22, "beruf": "Praktikantin",
     "budget_min": 500, "budget_max": 750, "raucher": False, "haustiere": False, "sauberkeit": 4,
     "bio": "Neu in der Stadt, freue mich auf nette Mitbewohner."},
    {"name": "Pascal Graf", "email": "pascal@example.com", "alter": 33, "beruf": "Projektleiter",
     "budget_min": 900, "budget_max": 1400, "raucher": True, "haustiere": False, "sauberkeit": 3,
     "bio": "Geselliger Typ, organisiere gerne WG-Abende."},
]

DUMMY_LISTINGS = [
    {
        "owner_email": "lena@example.com",
        "title": "Helles WG-Zimmer nahe Zürich HB",
        "description": "Freies Zimmer in einer ruhigen 3er-WG mit großem Balkon und gemeinsamer Küche.",
        "rent": 820,
        "deposit": 1600,
        "location": "Zürich, Kreis 4",
        "room_size": 18,
        "available_from": date(2026, 8, 1),
        "furnished": True,
        "pets_allowed": False,
        "smoking_allowed": False,
        "flatmates": 2,
        "photo_url": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85",
    },
    {
        "owner_email": "tim@example.com",
        "title": "Möblierte Wohnung mit Homeoffice-Platz",
        "description": "Modernes Apartment mit schnellem Internet, ideal für Homeoffice und ruhiges Arbeiten.",
        "rent": 1240,
        "deposit": 2400,
        "location": "Basel, Gundeldingen",
        "room_size": 32,
        "available_from": date(2026, 7, 15),
        "furnished": True,
        "pets_allowed": True,
        "smoking_allowed": False,
        "flatmates": 0,
        "photo_url": "https://images.unsplash.com/photo-1494526585095-c41746248156",
    },
    {
        "owner_email": "sara@example.com",
        "title": "Gemütliches Zimmer in gepflegter WG",
        "description": "Helles Zimmer mit Blick ins Grüne, ruhige Mitbewohner und gemeinsame Abendessen willkommen.",
        "rent": 760,
        "deposit": 1500,
        "location": "Bern, Länggasse",
        "room_size": 16,
        "available_from": date(2026, 9, 1),
        "furnished": False,
        "pets_allowed": False,
        "smoking_allowed": False,
        "flatmates": 3,
        "photo_url": "https://images.unsplash.com/photo-1484154218962-a197022b5858",
    },
    {
        "owner_email": "nina@example.com",
        "title": "Studio für Studierende",
        "description": "Kleines Studio in Uni-Nähe mit Küche und Bad, perfekt für den Start in der Stadt.",
        "rent": 690,
        "deposit": 1200,
        "location": "Zürich, Oerlikon",
        "room_size": 24,
        "available_from": date(2026, 8, 15),
        "furnished": True,
        "pets_allowed": False,
        "smoking_allowed": False,
        "flatmates": 0,
        "photo_url": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688",
    },
    {
        "owner_email": "pascal@example.com",
        "title": "Große Wohnung mit Gemeinschaftsraum",
        "description": "Helle Wohnung mit Platz für gemeinsame WG-Abende und guter Anbindung an den ÖV.",
        "rent": 1320,
        "deposit": 2600,
        "location": "Winterthur, Seen",
        "room_size": 48,
        "available_from": date(2026, 10, 1),
        "furnished": False,
        "pets_allowed": False,
        "smoking_allowed": True,
        "flatmates": 1,
        "photo_url": "https://images.unsplash.com/photo-1494526585095-c41746248156",
    },
]


def run():
    with app.app_context():
        db.drop_all()
        db.create_all()

        owner_emails = {listing["owner_email"] for listing in DUMMY_LISTINGS}
        users_by_email = {}
        for data in DUMMY_USERS:
            user = User(**data)
            user.rolle = "anbietend" if data["email"] in owner_emails else "suchend"
            user.set_password("test1234")
            db.session.add(user)
            users_by_email[user.email] = user
        db.session.commit()

        for data in DUMMY_LISTINGS:
            owner = users_by_email[data.pop("owner_email")]
            listing = Listing(owner=owner, **data)
            db.session.add(listing)
        db.session.commit()

        print(
            f"{len(DUMMY_USERS)} Dummy-User und {len(DUMMY_LISTINGS)} Dummy-Inserate angelegt. "
            "Login: lena@example.com / test1234"
        )


if __name__ == "__main__":
    run()
