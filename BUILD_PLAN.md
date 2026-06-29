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
4. Für Fotos: Storage → Bucket „listings" erstellen (Tag 3).
5. ⚠️ Projekt pausiert nach 7 Tagen Inaktivität → vor Bewertung im Dashboard reaktivieren.

## Build-Reihenfolge (Schritt für Schritt)

### Tag 1 — Fundament ✅ (Gerüst steht)
- [x] App-Factory, Models, Auth, eigenes Profil, Seed
- [x] Profil bearbeiten: Formular (Budget, Lifestyle, Bio, Foto-URL) in `profile.py`
- [x] Inserat erstellen: Formular + Route in `listings.py`
- [x] ER-Modell dokumentieren (Artefakt)

### Tag 2 — Grundfunktionen
- [x] `listings.py`: Detail-View mit Fotos ausbauen (Feature View)
- [ ] `search.py`: alle Filter (Preis, Zimmer, Ort, Verfügbarkeit) + Template
- [ ] `search.py`: `match_score()` ausbauen (Budget + Lifestyle gewichten) → Ergebnisse sortieren
- [ ] `chat.py`: Inbox-Übersicht + Chat-Template fertigstellen
- [ ] Foto-Upload zu Supabase Storage statt URL-Feld

### Tag 3 — Sonderfunktionen (min. 3) + Testing
- [ ] A: Favoriten speichern/entfernen + Favoriten-Liste
- [ ] B: Auf Inserat bewerben → `Application` + Status-Handling
- [ ] C: Email an Inserent bei Bewerbung → Resend HTTP-API (nicht SMTP!)
- [ ] D: Geo-Suche → Haversine-Distanz + Leaflet-Karte
- [ ] E: Besichtigungstermin → `Appointment` + Buchungs-UI
- [ ] Test-Prozeduren ausführen → priorisierte Bug-Liste

### Do–Sa — Deploy & Abgabe
- [ ] `gunicorn` Start-Command auf Render, `DATABASE_URL` als Env-Var
- [ ] Bugs fixen, UX polieren
- [ ] Video-Demo (max. 10 Min, alle sprechen), Tagebuch, GitHub-Release + duda/heej

## Wichtige Hinweise für die Umsetzung

- **Secrets**: nur via `.env` / Env-Vars, nie committen (`.env` ist in `.gitignore`).
- **Email**: Render-Free blockiert SMTP-Ports → Resend/SendGrid HTTP-API nutzen.
- **DB-Schema-Änderung**: `models.py` anpassen → bei `db.create_all()` werden neue Tabellen erstellt, aber **bestehende nicht migriert**. Im Zweifel `python seed.py` neu laufen lassen (löscht & baut neu) oder Flask-Migrate einführen.
- **Match-Score** muss kein ML sein — gewichteter Vergleich strukturierter Daten reicht laut Anforderung.
