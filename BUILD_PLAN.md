# FlatMate — Projektgerüst & Build-Plan

Ziel-Struktur und Feature-Liste (Schritt für Schritt ausgebaut). Aktueller Stand: siehe Häkchen unten und `changelog.md`.

## Ordnerstruktur

```
flatmate/
├── .env.example          # zu .env kopieren, Werte einsetzen
├── .gitignore
├── requirements.txt
├── render.yaml           # Render-Deployment (Blueprint)
├── config.py             # liest .env; SQLite-Fallback bzw. Supabase Postgres
├── main.py               # Einstiegspunkt (lokal: python main.py, deployed: gunicorn main:app)
├── seed.py               # 40 Dummy-User + 20 Inserate (fester Seed)
└── app/
    ├── __init__.py       # App-Factory, Blueprints, db.create_all(), Nav-Zähler
    ├── extensions.py     # db, login_manager
    ├── models.py         # User, Listing, Application, Message, Favorite, Appointment
    ├── forms.py          # WTForms (Login, Register, Profil, Inserat, Bewerbung, …)
    ├── email.py          # send_email() via SendGrid (Log-Fallback ohne Key)
    ├── storage.py        # Bild-Upload → Supabase Storage
    ├── routes/           # auth.py, profile.py, listings.py, chat.py
    ├── templates/        # base + _icons + auth/ profile/ listings/ chat/ email/
    └── static/css/       # style.css (Design-System, responsive)
```

## Setup (einmalig)

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env          # dann Supabase DATABASE_URL + SECRET_KEY eintragen
python seed.py                  # Tabellen + 40 Dummy-User / 20 Inserate
python main.py                  # http://127.0.0.1:5000
```

Login zum Testen: `lena@example.com` / `test1234`

## Supabase-Verbindung

1. supabase.com → Projekt erstellen.
2. Project Settings → Database → Connection string (URI) kopieren.
3. In `.env` als `DATABASE_URL` einsetzen, `[YOUR-PASSWORD]` ersetzen.
4. Für Fotos: Storage → öffentlichen Bucket „images" erstellen (Service-Key als `SUPABASE_STORAGE_KEY`).
5. ⚠️ Projekt pausiert nach 7 Tagen Inaktivität → vor Bewertung im Dashboard reaktivieren.

## Funktionsumfang (Schritt für Schritt)

Status: `[x]` fertig · `[ ]` offen

### Grundfunktionen (Pflicht — Basis für Note 4.0)

- [x] **Fundament**: App-Factory, Models, Auth (Register/Login/Logout), Seed
- [x] **View**: eigenes & fremdes Profil anzeigen, Profil bearbeiten
- [x] **Store**: Daten in DB — lokal SQLite, deployed Supabase Postgres (`DATABASE_URL`)
- [x] **ER-Modell** dokumentiert (Artefakt)
- [x] **Inserate**: erstellen/bearbeiten + Detail-View; Bild per Upload (Supabase Storage) oder URL
- [x] **Search**: Filter (Kanton, Ort, max. Miete, min. Zimmergrösse, Verfügbarkeit, Haustiere/Rauchen) in der Inserate-Übersicht (`listings.index`)
- [x] **Match**: passende Zimmer werden über die Inserate-Filter + Umkreissuche (Ort/Budget/Grösse/Verfügbarkeit/Lifestyle) zugeordnet
- [x] **Chat**: 1:1 Inbox-Übersicht + Konversation mit gespeicherten Nachrichten + Gelesen-Status (`chat.py`)

### Sonderfunktionen (mind. 3 wählen — mehr/besser = bessere Note)

- [x] **Favoriten** speichern/entfernen + Favoriten-Liste
- [x] **Besichtigungstermin** → `Appointment` + Buchungs-UI
- [x] **Bewerbung** auf Inserat → `Application` + Status (Inserent sieht Bewerber)
- [x] **Email** an Inserent bei Bewerbung → SendGrid HTTP-API, Single Sender (kein SMTP, keine Domain; Dev: Log-Fallback ohne Key)
- [x] **Kartenansicht**: Google Maps Detailkarte + `/listings/map` mit Markern und Detailpanel
- [x] **Geo-Suche**: Umkreissuche in km mit Haversine-Distanz und gespeicherten Koordinaten
- [x] **Foto-Upload**: Profil- & Inserat-Bilder in Supabase Storage (Bucket `images`) oder direkte Bild-URL
- [x] **Live-Chat**: Nachrichten per Polling (5 s) ohne Reload + Ungelesen-Badges in der Navigation
- [x] **Löschen**: eigenes Inserat und eigenes Konto (mit Bestätigung) entfernbar

### Testing, Deployment & Abgabe

- [x] Deployment auf Render vorbereitet (`render.yaml`, `gunicorn`, Env-Vars); Supabase Postgres als produktive DB
- [ ] Test-Prozeduren ausführen → priorisierte Bug-Liste
- [ ] Bugs fixen, UX polieren
- [ ] Video-Demo (max. 10 Min, alle sprechen), Tagebuch, GitHub-Release + duda/heej

## Wichtige Hinweise für die Umsetzung

- **Secrets**: nur via `.env` / Env-Vars, nie committen (`.env` ist in `.gitignore`).
- **Email**: Render-Free blockiert SMTP-Ports → Resend/SendGrid HTTP-API nutzen.
- **Google Maps**: API-Key nur via `.env` / Env-Var `GOOGLE_MAPS_API_KEY`; in Google Cloud auf erlaubte Domains und benoetigte APIs beschraenken.
- **DB-Schema-Änderung**: `models.py` anpassen → bei `db.create_all()` werden neue Tabellen erstellt, aber **bestehende nicht migriert**. Im Zweifel `python seed.py` neu laufen lassen (löscht & baut neu) oder Flask-Migrate einführen.
- **Ein Inserat pro User** (bewusste Vereinfachung): jeder User kann genau ein eigenes Inserat haben. „Neues Inserat" ist nur sichtbar, solange keines existiert; sonst führt „Mein Inserat" direkt dorthin.
