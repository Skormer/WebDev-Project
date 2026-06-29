# Changelog

Pro abgeschlossenem Schritt/Feature ein Eintrag.

## Schritt 0 — Projekt-Setup & Dokumentation (2026-06-29)

App-Idee **FlateMate** (WG-/Mitbewohner-Matching) gewählt und das Projektgerüst
samt Planungsunterlagen aufgesetzt.

**Hinzugefügt:**
- `PROJECT_GUIDELINES.md` — Kursvorgaben (ZHAW), Pflicht-/Sonderfunktionen, Bewertung, Abgaben
- `BUILD_PLAN.md` — Zielstruktur, Milestones, Tag-für-Tag-Reihenfolge der Features
- `temp_flatemate_er_diagram.html` — ER-Modell mit 7 Tabellen (User, Listing,
  ListingPhoto, Application, Favorite, Message, Appointment) als Mermaid-Diagramm
- `README.md` — Projektübersicht + Setup-Anleitung
- `CLAUDE.md` — Kontext/Anleitung für Claude Code

**Aufräumen:**
- `gitignore.txt` → als aktives `.gitignore` übernommen, `*.db` und `__pycache__/` ergänzt
- Versehentlich getracktes `__pycache__/` aus Git entfernt (`git rm --cached`)
- Kaputte Datei `_init_.py` (Einzel-Unterstrich) entfernt — Paket-Marker ist jetzt `app/__init__.py`

## Schritt 1 — Login & Profil aus DB (2026-06-29)

Lauffähiges Grundgerüst: Registrierung/Login mit gehashtem Passwort, und nach
dem Login das eigene Profil mit Daten aus der DB.

**Neu:**
- App-Factory (`app/__init__.py`) + Extensions (`app/extensions.py`: `db`, `login_manager`)
- `config.py` + `.env.example`: liest `.env`, nutzt **SQLite als Fallback**, wenn keine
  `DATABASE_URL` gesetzt ist (läuft sofort ohne Supabase-Setup)
- `app/models.py`: **nur `User`** (Login-/Profilfelder gemäss ER-Diagramm). Weitere
  Tabellen folgen in späteren Schritten.
- `app/routes/auth.py`: `register` / `login` / `logout` (Werkzeug Password-Hash)
- `app/routes/profile.py`: eigenes Profil (`/profile`) + fremdes Profil (`/profile/<id>`)
- `app/forms.py`: `LoginForm`, `RegisterForm` (Flask-WTF, CSRF aktiv)
- Templates: `base`, `auth/login`, `auth/register`, `profile` + `static/css/style.css`
- `seed.py`: legt Tabellen neu an und füllt **10 Dummy-User** (Login: `lena@example.com` / `test1234`)

**Abweichung vom BUILD_PLAN:** SQLite-Fallback statt zwingend Supabase, und vorerst
nur die `User`-Tabelle statt aller 7 (bewusst kleiner Schritt).

**Getestet:** Login (richtig/falsch), Profil-Anzeige mit DB-Daten, Logout,
Auth-Schutz (`/profile` → Redirect zu `/login`).
