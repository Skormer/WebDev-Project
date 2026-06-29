"""Legt die Tabellen neu an und füllt 10 Dummy-User ein.

    python seed.py

ACHTUNG: drop_all() löscht bestehende Daten. Login zum Testen:
    lena@example.com / test1234   (Passwort ist bei allen gleich)
"""

from app import create_app
from app.extensions import db
from app.models import User

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


def run():
    with app.app_context():
        db.drop_all()
        db.create_all()
        for data in DUMMY_USERS:
            user = User(**data)
            user.set_password("test1234")
            db.session.add(user)
        db.session.commit()
        print(f"{len(DUMMY_USERS)} Dummy-User angelegt. Login: lena@example.com / test1234")


if __name__ == "__main__":
    run()
