# FlateMate — Projektgerüst & Build-Plan

Lauffähiges Fundament bis Milestone M1 (Login + Profil aus DB). Restliche Features sind als Stubs mit `# TODO` markiert — Schritt für Schritt ausbauen.

## Ordnerstruktur

```
flatemate/
├── .env.example          # zu .env kopieren, Supabase-Werte einsetzen
├── .gitignore
├── requirements.txt
├── config.py             # liest .env, normalisiert DATABASE_URL
├── main.py               # Einstiegspunkt: flask --app main run
├── seed.py               # 10 Dummy-User + Inserate
└── app/
    ├── __init__.py       # App-Factory, Blueprints, db.create_all()
    ├── extensions.py     # db, login_manager
    ├── models.py         # alle 7 Tabellen
    ├── routes/
    │   ├── auth.py       # ✅ register/login/logout (fertig)
    │   ├── profile.py    # ✅ eigenes + fremdes Profil (fertig)
    │   ├── listings.py   # 🔧 Stub: index + detail, Rest TODO
    │   ├── search.py     # 🔧 Stub: Filter + match_score TODO
    │   └── chat.py       # 🔧 Stub: 1:1 Chat Grundgerüst
    ├── templates/        # base, auth/, profile (fertig); Rest TODO
    └── static/css/       # Platzhalter-CSS
```

## Setup (einmalig)

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env          # dann Supabase DATABASE_URL + SECRET_KEY eintragen
python seed.py                  # Tabellen + 10 Dummy-Inserate
flask --app main run
```

Login zum Testen: `lena@example.com` / `test1234`

## Supabase-Verbindung

1. supabase.com → Projekt erstellen.
2. Project Settings → Database → Connection string (URI) kopieren.
3. In `.env` als `DATABASE_URL` einsetzen, `[YOUR-PASSWORD]` ersetzen.
4. Für Fotos: Storage → Bucket „listings" erstellen (bei Sonderfunktion Foto-Upload).
5. ⚠️ Projekt pausiert nach 7 Tagen Inaktivität → vor Bewertung im Dashboard reaktivieren.

## Funktionsumfang (Schritt für Schritt)

Status: `[x]` fertig · `[ ]` offen

### Grundfunktionen (Pflicht — Basis für Note 4.0)

- [x] **Fundament**: App-Factory, Models, Auth (Register/Login/Logout), Seed
- [x] **View**: eigenes & fremdes Profil anzeigen, Profil bearbeiten
- [x] **Store**: Daten in DB persistieren (User, Listing)
- [x] **ER-Modell** dokumentiert (Artefakt)
- [x] **Inserate**: erstellen (`listings.py`) + Detail-View mit Fotos
- [x] **Search**: Filter (Kanton, Ort, max. Miete, min. Zimmergrösse, Verfügbarkeit, Haustiere/Rauchen) in der Inserate-Übersicht (`listings.index`)
- [ ] **Match**: `match_score()` ausbauen (Budget + Lifestyle gewichten) → Ergebnisse sortieren
- [x] **Chat**: 1:1 Inbox-Übersicht + Konversation mit gespeicherten Nachrichten + Gelesen-Status (`chat.py`)

### Sonderfunktionen (mind. 3 wählen — mehr/besser = bessere Note)

- [x] **Favoriten** speichern/entfernen + Favoriten-Liste
- [x] **Besichtigungstermin** → `Appointment` + Buchungs-UI
- [x] **Bewerbung** auf Inserat → `Application` + Status (Inserent sieht Bewerber)
- [x] **Email** an Inserent bei Bewerbung → SendGrid HTTP-API, Single Sender (kein SMTP, keine Domain; Dev: Log-Fallback ohne Key)
- [x] **Kartenansicht**: Google Maps Detailkarte + `/listings/map` mit Markern und Detailpanel
- [x] **Geo-Suche**: Umkreissuche in km mit Haversine-Distanz und gespeicherten Koordinaten
- [ ] **Foto-Upload** zu Supabase Storage statt URL-Feld

### Testing, Deployment & Abgabe

- [ ] Test-Prozeduren ausführen → priorisierte Bug-Liste
- [ ] `gunicorn` Start-Command auf Render, `DATABASE_URL` als Env-Var
- [ ] Bugs fixen, UX polieren
- [ ] Video-Demo (max. 10 Min, alle sprechen), Tagebuch, GitHub-Release + duda/heej

## Wichtige Hinweise für die Umsetzung

- **Secrets**: nur via `.env` / Env-Vars, nie committen (`.env` ist in `.gitignore`).
- **Email**: Render-Free blockiert SMTP-Ports → Resend/SendGrid HTTP-API nutzen.
- **Google Maps**: API-Key nur via `.env` / Env-Var `GOOGLE_MAPS_API_KEY`; in Google Cloud auf erlaubte Domains und benoetigte APIs beschraenken.
- **DB-Schema-Änderung**: `models.py` anpassen → bei `db.create_all()` werden neue Tabellen erstellt, aber **bestehende nicht migriert**. Im Zweifel `python seed.py` neu laufen lassen (löscht & baut neu) oder Flask-Migrate einführen.
- **Match-Score** muss kein ML sein — gewichteter Vergleich strukturierter Daten reicht laut Anforderung.
- **Ein Inserat pro User** (bewusste Vereinfachung): jeder User kann genau ein eigenes Inserat haben. „Neues Inserat" ist nur sichtbar, solange keines existiert; sonst führt „Mein Inserat" direkt dorthin.
