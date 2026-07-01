"""Tabellen neu anlegen und mit Dummy-Daten füllen (40 User, 20 Inserate).

    python seed.py           # nur gegen lokale SQLite-DB
    python seed.py --force   # nötig gegen externe DB (Supabase) — löscht ALLE Daten!

Test-Login: lena@example.com / test1234 (gleiches Passwort für alle).
"""

import random
import sys
from datetime import date

from app import create_app
from app.extensions import db
from app.models import Application, Listing, Message, User

app = create_app()
rng = random.Random(42)  # fester Seed → reproduzierbare Daten

USER_COUNT = 40
LISTING_COUNT = 20   # die ersten LISTING_COUNT User sind Inserenten (rolle "anbietend")
PASSWORD = "test1234"

CITIES = [
    {"stadt": "Zürich", "kanton": "ZH", "lat": 47.3769, "lng": 8.5417},
    {"stadt": "Genf", "kanton": "GE", "lat": 46.2044, "lng": 6.1432},
    {"stadt": "Basel", "kanton": "BS", "lat": 47.5596, "lng": 7.5886},
    {"stadt": "Bern", "kanton": "BE", "lat": 46.9480, "lng": 7.4474},
    {"stadt": "Lausanne", "kanton": "VD", "lat": 46.5197, "lng": 6.6323},
    {"stadt": "Winterthur", "kanton": "ZH", "lat": 47.5000, "lng": 8.7241},
    {"stadt": "Luzern", "kanton": "LU", "lat": 47.0502, "lng": 8.3093},
    {"stadt": "St. Gallen", "kanton": "SG", "lat": 47.4245, "lng": 9.3767},
    {"stadt": "Lugano", "kanton": "TI", "lat": 46.0037, "lng": 8.9511},
    {"stadt": "Zug", "kanton": "ZG", "lat": 47.1662, "lng": 8.5155},
    {"stadt": "Biel", "kanton": "BE", "lat": 47.1368, "lng": 7.2468},
    {"stadt": "Chur", "kanton": "GR", "lat": 46.8499, "lng": 9.5329},
    {"stadt": "Freiburg", "kanton": "FR", "lat": 46.8065, "lng": 7.1619},
    {"stadt": "Aarau", "kanton": "AG", "lat": 47.3925, "lng": 8.0442},
]
FIRST_NAMES = ["Lena", "Ben", "Clara", "Dario", "Emma", "Fabio", "Gina", "Hannes", "Ivana", "Jan",
               "Kira", "Luca", "Mia", "Noah", "Olivia", "Pablo", "Rahel", "Samuel", "Tessa", "Vera",
               "Yves", "Zoe", "Leon", "Sophie", "Elias", "Lara", "Nico", "Julia", "Fynn", "Maya"]
LAST_NAMES = ["Meier", "Baumann", "Christen", "Dubois", "Egli", "Favre", "Gerber", "Hofer", "Iten",
              "Jost", "Kunz", "Lehmann", "Moser", "Naef", "Odermatt", "Pfister", "Roth", "Suter",
              "Tanner", "Vogel", "Widmer", "Zimmermann", "Amrein", "Blaser", "Steiner"]
BERUFE = ["Studentin", "Student", "Pflegefachmann", "Informatikerin", "Verkäufer", "Designerin",
          "Elektriker", "Journalistin", "Koch", "Physiotherapeutin", "Lehrerin", "Musiker"]
NATIONEN = ["Schweiz", "Schweiz", "Schweiz", "Deutschland", "Italien", "Frankreich", "Österreich"]
HOBBIES = ["Wandern, Fotografie", "Gaming, Kochen", "Yoga, Lesen", "Velo, Bouldern",
           "Malen, Konzerte", "Joggen, Kaffee", "Fussball, Grillieren", "Tanzen, Sprachen"]
MUSIK = ["Indie, Pop", "Hip-Hop, Techno", "Rock, Jazz", "Klassik, Soul", "Electronic, House",
         "RnB, Afrobeats", "Folk, Country"]
WOCHENEND = ["ruhig", "unterwegs", "party", "gemischt"]
SOZIAL = ["fuer_mich", "gelegentlich", "gesellig"]
QUARTIERE = ["Zentrum", "Altstadt", "West", "Nord", "Süd", "Kreis 5", "Breite", "Vorstadt"]
STRASSEN = ["Bahnhofstrasse", "Hauptstrasse", "Seestrasse", "Bergweg", "Lindenweg", "Kirchgasse",
            "Sonnenweg", "Feldstrasse", "Poststrasse", "Rosenweg"]
TITEL_ADJ = ["Helles", "Gemütliches", "Modernes", "Grosses", "Zentrales", "Ruhiges", "Sonniges"]
PHOTOS = [
    "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85",
    "https://images.unsplash.com/photo-1494526585095-c41746248156",
    "https://images.unsplash.com/photo-1484154218962-a197022b5858",
    "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688",
    "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2",
    "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267",
    "https://images.unsplash.com/photo-1513694203232-719a280e022f",
]


def make_user(index):
    """Erzeugt einen Dummy-User. Index 0 ist der bekannte Demo-Login (lena@example.com)."""
    if index == 0:
        first, last, email = "Lena", "Meier", "lena@example.com"
    else:
        first, last = rng.choice(FIRST_NAMES), rng.choice(LAST_NAMES)
        email = f"{first.lower()}.{last.lower()}{index}@example.com"
    city = rng.choice(CITIES)
    budget_min = rng.choice([400, 500, 600, 700, 800])
    user = User(
        name=f"{first} {last}",
        email=email,
        alter=rng.randint(20, 45),
        beruf=rng.choice(BERUFE),
        stadt=city["stadt"],
        nationalitaet=rng.choice(NATIONEN),
        budget_min=budget_min,
        budget_max=budget_min + rng.choice([200, 300, 400, 500]),
        raucher=rng.random() < 0.25,
        haustiere=rng.random() < 0.3,
        sauberkeit=rng.randint(2, 5),
        hobbies=rng.choice(HOBBIES),
        musikgeschmack=rng.choice(MUSIK),
        wochenend_typ=rng.choice(WOCHENEND),
        soziales_level=rng.choice(SOZIAL),
        kocht_gern=rng.random() < 0.6,
        bio="Freue mich auf eine unkomplizierte, nette WG.",
        # Die ersten LISTING_COUNT User bieten ein Inserat an, der Rest sucht.
        rolle="anbietend" if index < LISTING_COUNT else "suchend",
    )
    user.set_password(PASSWORD)
    return user


def make_listing(owner):
    """Erzeugt ein Dummy-Inserat für den gegebenen Inserenten."""
    city = rng.choice(CITIES)
    rent = rng.choice([550, 650, 700, 780, 850, 950, 1050, 1150, 1250, 1400])
    return Listing(
        owner=owner,
        title=f"{rng.choice(TITEL_ADJ)} WG-Zimmer in {city['stadt']}",
        description="Schönes Zimmer in einer freundlichen WG mit guter ÖV-Anbindung.",
        rent=rent,
        deposit=rent * 2,
        kanton=city["kanton"],
        ort=f"{city['stadt']}, {rng.choice(QUARTIERE)}",
        strasse=f"{rng.choice(STRASSEN)} {rng.randint(1, 150)}",
        latitude=round(city["lat"] + rng.uniform(-0.02, 0.02), 5),
        longitude=round(city["lng"] + rng.uniform(-0.02, 0.02), 5),
        room_size=rng.randint(12, 40),
        available_from=date(2026, rng.randint(7, 12), rng.randint(1, 28)),
        furnished=rng.random() < 0.5,
        pets_allowed=rng.random() < 0.4,
        smoking_allowed=rng.random() < 0.3,
        flatmates=rng.randint(0, 4),
        photo_url=rng.choice(PHOTOS),
    )


def run():
    with app.app_context():
        db.drop_all()
        db.create_all()

        users = [make_user(i) for i in range(USER_COUNT)]
        listings = [make_listing(users[i]) for i in range(LISTING_COUNT)]
        db.session.add_all(users + listings)
        db.session.commit()

        # Ein paar Beispiel-Bewerbungen + -Nachrichten auf Lenas Inserat (Bezug per Index).
        owner, listing = users[0], listings[0]
        applicant_a, applicant_b = users[LISTING_COUNT], users[LISTING_COUNT + 1]
        db.session.add_all([
            Application(listing_id=listing.id, applicant_id=applicant_a.id,
                        nachricht="Hoi, ich hätte grosses Interesse am Zimmer!", status="offen"),
            Application(listing_id=listing.id, applicant_id=applicant_b.id,
                        nachricht="Wäre das Zimmer noch frei?", status="offen"),
            Message(sender_id=applicant_a.id, receiver_id=owner.id,
                    listing_id=listing.id, body="Hoi Lena, ist das Zimmer noch verfügbar?"),
            Message(sender_id=owner.id, receiver_id=applicant_a.id,
                    listing_id=listing.id, body="Hoi, ja gerne! Wann möchtest du es anschauen?"),
        ])
        db.session.commit()

        print(f"{len(users)} Dummy-User, {len(listings)} Dummy-Inserate, "
              "2 Bewerbungen und 2 Nachrichten angelegt. Login: lena@example.com / test1234")


if __name__ == "__main__":
    uri = app.config["SQLALCHEMY_DATABASE_URI"]
    if not uri.startswith("sqlite") and "--force" not in sys.argv:
        print("ABBRUCH: DATABASE_URL zeigt auf eine externe DB:")
        print(f"  {uri.split('@')[-1]}")
        print("seed.py löscht & überschreibt ALLE Tabellen — bei einer geteilten DB (Supabase)")
        print("verliert das ganze Team seine Daten. Wenn du das wirklich willst:  python seed.py --force")
        sys.exit(1)

    run()
