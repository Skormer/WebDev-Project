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

## Schritt 2 — Profil bearbeiten & Inserat erstellen (2026-06-29)

Erweiterung des Grundgerüsts um bearbeitbare Profile und das Erstellen von
Wohnungs-/Zimmerinseraten.

**Neu:**
- `app/forms.py`: `ProfileEditForm` und `ListingForm`
- `app/models.py`: `Listing`-Modell plus Beziehung `User.listings`
- `app/routes/profile.py`: `/profile/edit` speichert Budget, Lifestyle, Bio und Foto-URL
- `app/routes/listings.py`: `/listings/` Übersicht, `/listings/new` Formular zum Erstellen
- Templates: `profile_edit.html`, `listings/index.html`, `listings/new.html`
- Navigation + CSS für Inserate ergänzt

**Getestet:** Syntax-/Import-Check der geänderten Flask-Dateien ohne Fehler.

## Schritt 3 — ER-Modell dokumentiert (2026-06-29)

Das Datenmodell wurde als eigenes Artefakt dokumentiert und in die Projekt-
Unterlagen eingeordnet.

**Neu:**
- `temp_flatemate_er_diagram.html`: ER-Diagramm mit 7 Tabellen (User, Listing,
  ListingPhoto, Application, Favorite, Message, Appointment)
- `BUILD_PLAN.md`: ER-Modell als erledigt markiert

**Hinweis:** Das Diagramm ist als Browser-Artefakt abgelegt und wächst mit dem
Projekt mit.

## Schritt 4 — Profilbild-Upload als JPEG (2026-06-29)

Der Profilbild-Eintrag im Bearbeitungsformular wurde von einer URL-Eingabe auf
einen echten JPEG-Dateiupload umgestellt.

**Neu:**
- `app/forms.py`: Profilbild als `FileField` mit JPEG-Validierung
- `app/routes/profile.py`: hochgeladene Bilder werden unter `app/static/uploads/` gespeichert
- `app/templates/profile_edit.html`: `multipart/form-data` und Datei-Input
- `app/templates/base.html`: Link „Profil bearbeiten“ aus dem Header entfernt
- `.gitignore`: Upload-Ordner ignoriert

**Getestet:** Syntax-/Import-Check der geänderten Flask-Dateien ohne Fehler.
