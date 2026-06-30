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
- `app/routes/profile.py`: `/profile/edit` speichert Budget, Lifestyle, Bio und Profilbild
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

## Schritt 5 — Inserate-UI & Build-Plan überarbeitet (2026-06-29)

Verbesserte Darstellung der Inserate-Übersicht und neue Startseite.

**Neu:**
- `BUILD_PLAN.md`: Gliederung von Tagen auf **Grundfunktionen / Sonderfunktionen** umgestellt
- `app/templates/listings/index.html`: Karten sind kein Hyperlink mehr, sondern haben einen
  **„Details ansehen"-Button**
- `app/static/css/style.css`: Inserate-Grid responsiv — **3 pro Reihe ab 900px**, 2 ab 600px,
  1 darunter; breiteres Layout (`container-wide`, max. 1100px)
- `app/templates/base.html`: `main` nimmt eine optionale Seitenklasse (`main_class`-Block)
- `app/__init__.py`: Startseite (Logo) zeigt eingeloggt jetzt die **Inserate** statt des Profils
- `app/static/css/style.css`: Links global ohne Unterstrich (nur beim Hover), `container-wide`
  auf **1200px** erhöht, Buttons sauber (`text-decoration: none`)
- **Neues User-Feld `rolle`** (`suchend` / `anbietend`), um eindeutig zu zeigen, ob jemand
  ein Inserat anbietet oder auf Wohnungssuche ist:
  - `app/models.py`: Spalte `rolle` (Default `suchend`)
  - `app/forms.py`: `SelectField` „Status" im Profil-Bearbeiten-Formular
  - `app/routes/profile.py`: speichert `rolle`
  - `app/templates/profile.html` + `listings/detail.html`: farbiges Status-Badge
  - `seed.py`: Inserenten → `anbietend`, restliche User → `suchend`

**Aufräumen / Anpassungen:**
- `app/models.py`: ungenutzte Felder `lat` / `lng` beim `User` entfernt (`Listing` hatte keine)
- **Neue User-Felder `stadt` + `nationalitaet`** (Eingabe im Bearbeiten-Formular, Anzeige im Profil
  und in der Inserent-Karte; Werte in `seed.py` ergänzt)
- Inserat-Detail (Inserent-Karte): Status-Badge „Bietet ein Inserat an" entfernt (ohnehin klar)
  und Budget ausgeblendet (Inserent sucht Mitbewohner, kein Zimmer) — stattdessen Stadt/Nationalität
- `style.css`: doppelte `display: inline-block;` in `.btn` entfernt

**Getestet:** App-Boot + Test-Client: `/` → `/listings/` (eingeloggt), Inserate-Grid mit
Buttons; Profil zeigt Status-Badge, Stadt & Nationalität; Inserent-Karte ohne Badge/Budget;
Bearbeiten-Formular wählt den aktuellen Status vor und speichert Änderungen. `lat`/`lng` aus
dem Schema entfernt, `stadt`/`nationalitaet` vorhanden. DB neu geseedet (Schema-Änderung).
