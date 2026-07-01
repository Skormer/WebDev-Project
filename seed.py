"""Legt die Tabellen neu an und füllt 10 Dummy-User plus Dummy-Inserate ein.

    python seed.py            # nur gegen lokale SQLite-DB erlaubt
    python seed.py --force    # nötig, wenn DATABASE_URL auf eine externe DB zeigt (z. B. Supabase)

ACHTUNG: drop_all() löscht ALLE Daten. Bei einer geteilten DB (Supabase) trifft das das
ganze Team — deshalb der --force-Schutz unten. Login zum Testen:
    lena@example.com / test1234   (Passwort ist bei allen gleich)
"""

import sys
from datetime import date

from app import create_app
from app.extensions import db
from app.models import Application, Listing, Message, User

app = create_app()

DUMMY_USERS = [
    {"name": "Lena Meier", "email": "lena@example.com", "alter": 24, "beruf": "Studentin",
     "stadt": "Zürich", "nationalitaet": "Schweiz",
     "budget_min": 600, "budget_max": 900, "raucher": False, "haustiere": False, "sauberkeit": 4,
     "bio": "Suche eine WG in Zürich, mag Kochen und Klettern."},
    {"name": "Tim Brunner", "email": "tim@example.com", "alter": 28, "beruf": "Software Engineer",
     "stadt": "Basel", "nationalitaet": "Schweiz",
     "budget_min": 800, "budget_max": 1200, "raucher": False, "haustiere": True, "sauberkeit": 3,
     "bio": "Ruhiger Mitbewohner mit Katze, arbeite oft im Homeoffice."},
    {"name": "Sara Keller", "email": "sara@example.com", "alter": 31, "beruf": "Lehrerin",
     "stadt": "Bern", "nationalitaet": "Schweiz",
     "budget_min": 700, "budget_max": 1000, "raucher": False, "haustiere": False, "sauberkeit": 5,
     "bio": "Ordnungsliebend, gerne gemeinsame Abendessen."},
    {"name": "Marco Rossi", "email": "marco@example.com", "alter": 26, "beruf": "Grafiker",
     "stadt": "Lugano", "nationalitaet": "Italien",
     "budget_min": 500, "budget_max": 800, "raucher": True, "haustiere": False, "sauberkeit": 2,
     "bio": "Kreativ, Nachtmensch, spiele Gitarre."},
    {"name": "Nina Huber", "email": "nina@example.com", "alter": 23, "beruf": "Studentin",
     "stadt": "Zürich", "nationalitaet": "Schweiz",
     "budget_min": 550, "budget_max": 850, "raucher": False, "haustiere": False, "sauberkeit": 4,
     "bio": "Sportlich, suche eine unkomplizierte WG nahe der Uni."},
    {"name": "David Frei", "email": "david@example.com", "alter": 35, "beruf": "Architekt",
     "stadt": "Zug", "nationalitaet": "Schweiz",
     "budget_min": 1000, "budget_max": 1500, "raucher": False, "haustiere": False, "sauberkeit": 4,
     "bio": "Reise viel, brauche vor allem einen guten Schlafplatz."},
    {"name": "Elif Yilmaz", "email": "elif@example.com", "alter": 29, "beruf": "Krankenpflegerin",
     "stadt": "Basel", "nationalitaet": "Türkei",
     "budget_min": 700, "budget_max": 1100, "raucher": False, "haustiere": True, "sauberkeit": 3,
     "bio": "Schichtarbeit, daher manchmal tagsüber zuhause. Habe einen Hund."},
    {"name": "Jonas Weber", "email": "jonas@example.com", "alter": 27, "beruf": "Doktorand",
     "stadt": "Bern", "nationalitaet": "Deutschland",
     "budget_min": 600, "budget_max": 950, "raucher": False, "haustiere": False, "sauberkeit": 3,
     "bio": "Lese gerne, koche viel vegetarisch."},
    {"name": "Aline Roth", "email": "aline@example.com", "alter": 22, "beruf": "Praktikantin",
     "stadt": "Lausanne", "nationalitaet": "Schweiz",
     "budget_min": 500, "budget_max": 750, "raucher": False, "haustiere": False, "sauberkeit": 4,
     "bio": "Neu in der Stadt, freue mich auf nette Mitbewohner."},
    {"name": "Pascal Graf", "email": "pascal@example.com", "alter": 33, "beruf": "Projektleiter",
     "stadt": "Winterthur", "nationalitaet": "Schweiz",
     "budget_min": 900, "budget_max": 1400, "raucher": True, "haustiere": False, "sauberkeit": 3,
     "bio": "Geselliger Typ, organisiere gerne WG-Abende."},
]

DUMMY_LISTINGS = [
    {
        "owner_email": "lena@example.com",
        "title": "Helles WG-Zimmer nahe Zürich HB",
        "description": "Freies Zimmer in einer ruhigen 3er-WG mit grossem Balkon und gemeinsamer Küche.",
        "rent": 820,
        "deposit": 1600,
        "kanton": "ZH",
        "ort": "Zürich, Kreis 4",
        "strasse": "Langstrasse 12",
        "latitude": 47.3782,
        "longitude": 8.5265,
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
        "kanton": "BS",
        "ort": "Basel, Gundeldingen",
        "strasse": "Gueterstrasse 88",
        "latitude": 47.5436,
        "longitude": 7.5892,
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
        "kanton": "BE",
        "ort": "Bern, Länggasse",
        "strasse": "Mittelstrasse 20",
        "latitude": 46.9541,
        "longitude": 7.4334,
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
        "kanton": "ZH",
        "ort": "Zürich, Oerlikon",
        "strasse": "Schaffhauserstrasse 310",
        "latitude": 47.4107,
        "longitude": 8.5445,
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
        "title": "Grosse Wohnung mit Gemeinschaftsraum",
        "description": "Helle Wohnung mit Platz für gemeinsame WG-Abende und guter Anbindung an den ÖV.",
        "rent": 1320,
        "deposit": 2600,
        "kanton": "ZH",
        "ort": "Winterthur, Seen",
        "strasse": "Tosstalstrasse 45",
        "latitude": 47.4821,
        "longitude": 8.7656,
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

        listings_by_owner = {}
        for data in DUMMY_LISTINGS:
            owner = users_by_email[data.pop("owner_email")]
            listing = Listing(owner=owner, **data)
            db.session.add(listing)
            listings_by_owner.setdefault(owner.email, listing)
        db.session.commit()

        # Ein paar Bewerbungen + Nachrichten zum Ausprobieren
        lena_listing = listings_by_owner["lena@example.com"]
        nina_listing = listings_by_owner["nina@example.com"]
        db.session.add_all([
            Application(listing_id=lena_listing.id, applicant_id=users_by_email["marco@example.com"].id,
                        nachricht="Hoi Lena, ich hätte grosses Interesse am Zimmer!", status="offen"),
            Application(listing_id=lena_listing.id, applicant_id=users_by_email["jonas@example.com"].id,
                        nachricht="Wäre das Zimmer noch frei? Ich bin ruhig und unkompliziert.", status="offen"),
            Application(listing_id=nina_listing.id, applicant_id=users_by_email["aline@example.com"].id,
                        status="offen"),
        ])
        db.session.add_all([
            Message(sender_id=users_by_email["marco@example.com"].id,
                    receiver_id=users_by_email["lena@example.com"].id,
                    listing_id=lena_listing.id, body="Hoi Lena, ist das Zimmer noch verfügbar?"),
            Message(sender_id=users_by_email["lena@example.com"].id,
                    receiver_id=users_by_email["marco@example.com"].id,
                    listing_id=lena_listing.id, body="Hoi Marco, ja gerne! Wann möchtest du es anschauen?"),
        ])
        db.session.commit()

        print(
            f"{len(DUMMY_USERS)} Dummy-User, {len(DUMMY_LISTINGS)} Dummy-Inserate, "
            "3 Bewerbungen und 2 Nachrichten angelegt. Login: lena@example.com / test1234"
        )


if __name__ == "__main__":
    uri = app.config["SQLALCHEMY_DATABASE_URI"]
    is_sqlite = uri.startswith("sqlite")
    force = "--force" in sys.argv

    if not is_sqlite and not force:
        target = uri.split("@")[-1]  # ohne Zugangsdaten
        print("ABBRUCH: DATABASE_URL zeigt auf eine externe DB:")
        print(f"  {target}")
        print("seed.py löscht & überschreibt ALLE Tabellen — bei einer geteilten DB (Supabase)")
        print("verliert das ganze Team seine Daten.")
        print("Wenn du das wirklich willst:  python seed.py --force")
        sys.exit(1)

    run()
