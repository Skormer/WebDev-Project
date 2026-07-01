"""Legt die Tabellen neu an und füllt 10 Dummy-User plus Dummy-Inserate ein.

    python seed.py            # nur gegen lokale SQLite-DB erlaubt
    python seed.py --force    # nötig, wenn DATABASE_URL auf eine externe DB zeigt (z. B. Supabase)

ACHTUNG: drop_all() löscht ALLE Daten. Bei einer geteilten DB (Supabase) trifft das das
ganze Team — deshalb der --force-Schutz unten. Login zum Testen:
    lena@example.com / test1234   (Passwort ist bei allen gleich)
"""

import random
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
     "hobbies": "Kochen, Klettern, Flohmaerkte", "musikgeschmack": "Indie, Pop",
     "wochenend_typ": "unterwegs", "soziales_level": "gelegentlich", "kocht_gern": True,
     "bio": "Suche eine WG in Zürich, mag Kochen und Klettern."},
    {"name": "Tim Brunner", "email": "tim@example.com", "alter": 28, "beruf": "Software Engineer",
     "stadt": "Basel", "nationalitaet": "Schweiz",
     "budget_min": 800, "budget_max": 1200, "raucher": False, "haustiere": True, "sauberkeit": 3,
     "hobbies": "Gaming, Serien, Spaziergaenge mit Katze", "musikgeschmack": "Lo-Fi, Rock",
     "wochenend_typ": "ruhig", "soziales_level": "fuer_mich", "kocht_gern": False,
     "bio": "Ruhiger Mitbewohner mit Katze, arbeite oft im Homeoffice."},
    {"name": "Sara Keller", "email": "sara@example.com", "alter": 31, "beruf": "Lehrerin",
     "stadt": "Bern", "nationalitaet": "Schweiz",
     "budget_min": 700, "budget_max": 1000, "raucher": False, "haustiere": False, "sauberkeit": 5,
     "hobbies": "Backen, Wandern, Brettspiele", "musikgeschmack": "Soul, Singer-Songwriter",
     "wochenend_typ": "gemischt", "soziales_level": "gesellig", "kocht_gern": True,
     "bio": "Ordnungsliebend, gerne gemeinsame Abendessen."},
    {"name": "Marco Rossi", "email": "marco@example.com", "alter": 26, "beruf": "Grafiker",
     "stadt": "Lugano", "nationalitaet": "Italien",
     "budget_min": 500, "budget_max": 800, "raucher": True, "haustiere": False, "sauberkeit": 2,
     "hobbies": "Gitarre, Design, Konzerte", "musikgeschmack": "Rock, Jazz",
     "wochenend_typ": "party", "soziales_level": "gesellig", "kocht_gern": True,
     "bio": "Kreativ, Nachtmensch, spiele Gitarre."},
    {"name": "Nina Huber", "email": "nina@example.com", "alter": 23, "beruf": "Studentin",
     "stadt": "Zürich", "nationalitaet": "Schweiz",
     "budget_min": 550, "budget_max": 850, "raucher": False, "haustiere": False, "sauberkeit": 4,
     "hobbies": "Joggen, Yoga, Kaffee", "musikgeschmack": "Pop, RnB",
     "wochenend_typ": "unterwegs", "soziales_level": "gelegentlich", "kocht_gern": False,
     "bio": "Sportlich, suche eine unkomplizierte WG nahe der Uni."},
    {"name": "David Frei", "email": "david@example.com", "alter": 35, "beruf": "Architekt",
     "stadt": "Zug", "nationalitaet": "Schweiz",
     "budget_min": 1000, "budget_max": 1500, "raucher": False, "haustiere": False, "sauberkeit": 4,
     "hobbies": "Reisen, Architektur, Fotografie", "musikgeschmack": "Electronic, Ambient",
     "wochenend_typ": "unterwegs", "soziales_level": "fuer_mich", "kocht_gern": False,
     "bio": "Reise viel, brauche vor allem einen guten Schlafplatz."},
    {"name": "Elif Yilmaz", "email": "elif@example.com", "alter": 29, "beruf": "Krankenpflegerin",
     "stadt": "Basel", "nationalitaet": "Türkei",
     "budget_min": 700, "budget_max": 1100, "raucher": False, "haustiere": True, "sauberkeit": 3,
     "hobbies": "Hundetraining, Serien, Kaffee", "musikgeschmack": "Pop, Turkish Pop",
     "wochenend_typ": "ruhig", "soziales_level": "gelegentlich", "kocht_gern": True,
     "bio": "Schichtarbeit, daher manchmal tagsüber zuhause. Habe einen Hund."},
    {"name": "Jonas Weber", "email": "jonas@example.com", "alter": 27, "beruf": "Doktorand",
     "stadt": "Bern", "nationalitaet": "Deutschland",
     "budget_min": 600, "budget_max": 950, "raucher": False, "haustiere": False, "sauberkeit": 3,
     "hobbies": "Lesen, vegetarisch kochen, Kino", "musikgeschmack": "Classical, Indie",
     "wochenend_typ": "ruhig", "soziales_level": "gelegentlich", "kocht_gern": True,
     "bio": "Lese gerne, koche viel vegetarisch."},
    {"name": "Aline Roth", "email": "aline@example.com", "alter": 22, "beruf": "Praktikantin",
     "stadt": "Lausanne", "nationalitaet": "Schweiz",
     "budget_min": 500, "budget_max": 750, "raucher": False, "haustiere": False, "sauberkeit": 4,
     "hobbies": "Sprachen, Tanzen, Ausstellungen", "musikgeschmack": "Afrobeats, Pop",
     "wochenend_typ": "gemischt", "soziales_level": "gesellig", "kocht_gern": False,
     "bio": "Neu in der Stadt, freue mich auf nette Mitbewohner."},
    {"name": "Pascal Graf", "email": "pascal@example.com", "alter": 33, "beruf": "Projektleiter",
     "stadt": "Winterthur", "nationalitaet": "Schweiz",
     "budget_min": 900, "budget_max": 1400, "raucher": True, "haustiere": False, "sauberkeit": 3,
     "hobbies": "WG-Abende, Fussball, Grillieren", "musikgeschmack": "Hip-Hop, Techno",
     "wochenend_typ": "party", "soziales_level": "gesellig", "kocht_gern": True,
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
    {
        "owner_email": "marco@example.com",
        "title": "Kreatives WG-Zimmer in Lugano",
        "description": "Zimmer in einer lebendigen 4er-WG mit Atelier-Ecke, viel Licht und kurzer Distanz zum See.",
        "rent": 640,
        "deposit": 1200,
        "kanton": "TI",
        "ort": "Lugano, Molino Nuovo",
        "strasse": "Via Trevano 22",
        "latitude": 46.0137,
        "longitude": 8.9558,
        "room_size": 14,
        "available_from": date(2026, 7, 20),
        "furnished": False,
        "pets_allowed": False,
        "smoking_allowed": True,
        "flatmates": 3,
        "photo_url": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267",
    },
    {
        "owner_email": "david@example.com",
        "title": "Ruhiges Zimmer in Zug mit eigenem Bad",
        "description": "Sehr ruhiges Zimmer in moderner Wohnung, ideal fuer Pendler oder konzentriertes Arbeiten.",
        "rent": 1180,
        "deposit": 2200,
        "kanton": "ZG",
        "ort": "Zug, Neustadt",
        "strasse": "Baarerstrasse 57",
        "latitude": 47.1748,
        "longitude": 8.5177,
        "room_size": 22,
        "available_from": date(2026, 8, 10),
        "furnished": True,
        "pets_allowed": False,
        "smoking_allowed": False,
        "flatmates": 1,
        "photo_url": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2",
    },
    {
        "owner_email": "elif@example.com",
        "title": "Haustierfreundliches Zimmer in Basel",
        "description": "Gemutliches Zimmer in entspannter WG, Hunde und Katzen sind willkommen.",
        "rent": 890,
        "deposit": 1700,
        "kanton": "BS",
        "ort": "Basel, St. Johann",
        "strasse": "Elsaesserstrasse 101",
        "latitude": 47.5704,
        "longitude": 7.5733,
        "room_size": 19,
        "available_from": date(2026, 9, 15),
        "furnished": False,
        "pets_allowed": True,
        "smoking_allowed": False,
        "flatmates": 2,
        "photo_url": "https://images.unsplash.com/photo-1489171078254-c3365d6e359f",
    },
    {
        "owner_email": "aline@example.com",
        "title": "Zentrales Zimmer in Lausanne",
        "description": "Moebliertes Zimmer nahe Bahnhof, internationale WG und unkomplizierte Uebergabe.",
        "rent": 740,
        "deposit": 1400,
        "kanton": "VD",
        "ort": "Lausanne, Centre",
        "strasse": "Rue du Simplon 15",
        "latitude": 46.5173,
        "longitude": 6.6296,
        "room_size": 15,
        "available_from": date(2026, 7, 5),
        "furnished": True,
        "pets_allowed": True,
        "smoking_allowed": True,
        "flatmates": 4,
        "photo_url": "https://images.unsplash.com/photo-1536376072261-38c75010e6c9",
    },
    {
        "owner_email": "jonas@example.com",
        "title": "Altbauzimmer in Bern Laenggasse",
        "description": "Grosses Altbauzimmer mit Parkett, ruhige Lage und vegetarische WG-Kueche.",
        "rent": 930,
        "deposit": 1800,
        "kanton": "BE",
        "ort": "Bern, Laenggasse",
        "strasse": "Gesellschaftsstrasse 36",
        "latitude": 46.9546,
        "longitude": 7.4279,
        "room_size": 25,
        "available_from": date(2026, 11, 1),
        "furnished": False,
        "pets_allowed": False,
        "smoking_allowed": False,
        "flatmates": 2,
        "photo_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f",
    },
]


# ---------------------------------------------------------------------------
# Zusätzliche, generierte Dummy-Daten (damit die App/Filter gefüllt sind).
# Reproduzierbar dank festem Seed. Ziel: 40 User total, 20 Inserate total.
# ---------------------------------------------------------------------------
_rng = random.Random(42)

_CITIES = [
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
    {"stadt": "Luzern", "kanton": "LU", "lat": 47.0502, "lng": 8.3093},
    {"stadt": "Aarau", "kanton": "AG", "lat": 47.3925, "lng": 8.0442},
]
_FIRST = ["Anna", "Ben", "Clara", "Dario", "Emma", "Fabio", "Gina", "Hannes", "Ivana", "Jan",
          "Kira", "Luca", "Mia", "Noah", "Olivia", "Pablo", "Rahel", "Samuel", "Tessa", "Vera",
          "Yves", "Zoe", "Leon", "Sophie", "Elias", "Lara", "Nico", "Julia", "Fynn", "Maya"]
_LAST = ["Baumann", "Christen", "Dubois", "Egli", "Favre", "Gerber", "Hofer", "Iten", "Jost",
         "Kunz", "Lehmann", "Moser", "Naef", "Odermatt", "Pfister", "Roth", "Suter", "Tanner",
         "Vogel", "Widmer", "Zimmermann", "Amrein", "Blaser", "Caduff", "Steiner"]
_BERUFE = ["Studentin", "Student", "Pflegefachmann", "Informatikerin", "Verkäufer", "Designerin",
           "Elektriker", "Journalistin", "Koch", "Physiotherapeutin", "Bankangestellter",
           "Lehrerin", "Mechaniker", "Biologin", "Musiker"]
_NATIONEN = ["Schweiz", "Schweiz", "Schweiz", "Deutschland", "Italien", "Frankreich",
             "Österreich", "Portugal", "Spanien"]
_HOBBIES = ["Wandern, Fotografie", "Gaming, Kochen", "Yoga, Lesen", "Velo, Bouldern",
            "Malen, Konzerte", "Joggen, Kaffee", "Fussball, Grillieren", "Tanzen, Sprachen",
            "Gärtnern, Backen", "Schwimmen, Filme"]
_MUSIK = ["Indie, Pop", "Hip-Hop, Techno", "Rock, Jazz", "Klassik, Soul", "Electronic, House",
          "RnB, Afrobeats", "Metal, Punk", "Folk, Country"]
_WOCHENEND = ["ruhig", "unterwegs", "party", "gemischt"]
_SOZIAL = ["fuer_mich", "gelegentlich", "gesellig"]
_QUARTIERE = ["Zentrum", "Altstadt", "West", "Nord", "Süd", "Ost", "Kreis 5", "Breite", "Vorstadt"]
_STRASSEN = ["Bahnhofstrasse", "Hauptstrasse", "Seestrasse", "Bergweg", "Lindenweg", "Kirchgasse",
             "Sonnenweg", "Feldstrasse", "Poststrasse", "Rosenweg"]
_TITEL_ADJ = ["Helles", "Gemütliches", "Modernes", "Grosses", "Zentrales", "Ruhiges", "Sonniges", "Charmantes"]
_PHOTOS = [
    "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85",
    "https://images.unsplash.com/photo-1494526585095-c41746248156",
    "https://images.unsplash.com/photo-1484154218962-a197022b5858",
    "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688",
    "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2",
    "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267",
    "https://images.unsplash.com/photo-1513694203232-719a280e022f",
]


def _build_extra(existing_emails):
    """Erzeugt zusätzliche User + Inserate, bis 40 User / 20 Inserate erreicht sind."""
    extra_users = []
    seen = set(existing_emails)
    target_extra_users = 40 - len(DUMMY_USERS)
    while len(extra_users) < target_extra_users:
        first = _rng.choice(_FIRST)
        last = _rng.choice(_LAST)
        email = f"{first.lower()}.{last.lower()}{len(extra_users) + 11}@example.com"
        if email in seen:
            continue
        seen.add(email)
        city = _rng.choice(_CITIES)
        budget_min = _rng.choice([400, 500, 600, 700, 800])
        extra_users.append({
            "name": f"{first} {last}",
            "email": email,
            "alter": _rng.randint(20, 45),
            "beruf": _rng.choice(_BERUFE),
            "stadt": city["stadt"],
            "nationalitaet": _rng.choice(_NATIONEN),
            "budget_min": budget_min,
            "budget_max": budget_min + _rng.choice([200, 300, 400, 500]),
            "raucher": _rng.random() < 0.25,
            "haustiere": _rng.random() < 0.3,
            "sauberkeit": _rng.randint(2, 5),
            "hobbies": _rng.choice(_HOBBIES),
            "musikgeschmack": _rng.choice(_MUSIK),
            "wochenend_typ": _rng.choice(_WOCHENEND),
            "soziales_level": _rng.choice(_SOZIAL),
            "kocht_gern": _rng.random() < 0.6,
            "bio": "Freue mich auf eine unkomplizierte, nette WG.",
        })

    # 10 zusätzliche Inserate → total 20; jeweils ein eigener Inserent (anbietend).
    extra_listings = []
    target_extra_listings = 20 - len(DUMMY_LISTINGS)
    for i in range(target_extra_listings):
        owner = extra_users[i]
        city = _rng.choice(_CITIES)
        rent = _rng.choice([550, 650, 700, 780, 850, 950, 1050, 1150, 1250, 1400])
        extra_listings.append({
            "owner_email": owner["email"],
            "title": f"{_rng.choice(_TITEL_ADJ)} WG-Zimmer in {city['stadt']}",
            "description": "Schönes Zimmer in einer freundlichen WG mit guter ÖV-Anbindung.",
            "rent": rent,
            "deposit": rent * 2,
            "kanton": city["kanton"],
            "ort": f"{city['stadt']}, {_rng.choice(_QUARTIERE)}",
            "strasse": f"{_rng.choice(_STRASSEN)} {_rng.randint(1, 150)}",
            "latitude": round(city["lat"] + _rng.uniform(-0.02, 0.02), 5),
            "longitude": round(city["lng"] + _rng.uniform(-0.02, 0.02), 5),
            "room_size": _rng.randint(12, 40),
            "available_from": date(2026, _rng.randint(7, 12), _rng.randint(1, 28)),
            "furnished": _rng.random() < 0.5,
            "pets_allowed": _rng.random() < 0.4,
            "smoking_allowed": _rng.random() < 0.3,
            "flatmates": _rng.randint(0, 4),
            "photo_url": _rng.choice(_PHOTOS),
        })
    return extra_users, extra_listings


def run():
    with app.app_context():
        db.drop_all()
        db.create_all()

        extra_users, extra_listings = _build_extra({u["email"] for u in DUMMY_USERS})
        all_users = DUMMY_USERS + extra_users
        all_listings = DUMMY_LISTINGS + extra_listings

        owner_emails = {listing["owner_email"] for listing in all_listings}
        users_by_email = {}
        for data in all_users:
            user = User(**data)
            user.rolle = "anbietend" if data["email"] in owner_emails else "suchend"
            user.set_password("test1234")
            db.session.add(user)
            users_by_email[user.email] = user
        db.session.commit()

        listings_by_owner = {}
        for data in all_listings:
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
            f"{len(all_users)} Dummy-User, {len(all_listings)} Dummy-Inserate, "
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
