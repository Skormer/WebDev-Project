# Changelog

Pro abgeschlossenem Schritt/Feature ein Eintrag.

## Schritt 0 — Projekt-Setup & Dokumentation (2026-06-29)

App-Idee **FlatMate** (WG-/Mitbewohner-Matching) gewählt und das Projektgerüst
samt Planungsunterlagen aufgesetzt.

**Hinzugefügt:**
- `PROJECT_GUIDELINES.md` — Kursvorgaben (ZHAW), Pflicht-/Sonderfunktionen, Bewertung, Abgaben
- `BUILD_PLAN.md` — Zielstruktur, Milestones, Tag-für-Tag-Reihenfolge der Features
- `temp_flatmate_er_diagram.html` — ER-Modell mit 7 Tabellen (User, Listing,
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
- `temp_flatmate_er_diagram.html`: ER-Diagramm mit 7 Tabellen (User, Listing,
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

## Schritt 6 — Inserate filtern und Adressmodell erweitert (2026-06-30)

Die Inserate-Übersicht wurde um Filter erweitert und das Listing-Ortsmodell wurde präziser gemacht.

**Neu / geändert:**
- `Listing.location` wurde durch `kanton`, `ort` und `strasse` ersetzt.
- `seed.py`: Dummy-Inserate enthalten Kanton, Ort, Strasse und wieder die ursprünglichen Unsplash-Bild-URLs.
- `app/routes/listings.py`: Filter für Kanton, Ort, maximale Miete, minimale Zimmergrösse, Verfügbarkeit, Haustiere und Rauchen.
- `app/templates/listings/index.html`: Kanton-Dropdown, Slider für maximale Miete und minimale Zimmergrösse, Checkboxen für Haustiere/Rauchen.
- Max-Miete-Slider: 50 bis 3000 CHF; 3000 bedeutet `3000+` und setzt kein oberes Limit.
- `app/templates/listings/new.html`: Eingabefelder für Kanton, Ort und Strasse.
- `app/templates/listings/detail.html`: Anzeige von Kanton, Ort und Strasse, Umlaute bereinigt.
- `app/static/css/style.css`: Styling für Filterpanel, Slider, Checkboxen und Reset-Button.

**Getestet:** Syntax-/Import-Check, Datenbank neu geseedet und Test-Client-Checks für `/listings/`, Filter-URLs, `/listings/new` und `/listings/1`.

## Schritt 7 — Bewerbungen & Chat (2026-06-30)

Zwei neue Funktionen: auf ein Inserat bewerben und 1:1-Chat mit gespeicherten Nachrichten.

**Neu — Bewerbung (`Application`):**
- `app/models.py`: Tabelle `Application` (listing/applicant/nachricht/status/created_at),
  Unique-Constraint pro (Inserat, Bewerber)
- `app/forms.py`: `ApplicationForm` (optionale Nachricht)
- `app/routes/listings.py`: Button **„Für Inserat bewerben"** (`/listings/<id>/apply`),
  verhindert Doppel- und Eigenbewerbung; Bewerber sieht seinen Status im Detail
- **Ein Inserat pro User**: „Neues Inserat" nur ohne eigenes Inserat sichtbar, sonst
  Nav-Link **„Mein Inserat"** direkt zum eigenen Inserat
- Eigenes Inserat: oben Button **„Bewerbungen (N)"** → eigene Seite
  (`/listings/<id>/applications`) mit offenen Bewerbungen (Profil, Nachricht, **Ablehnen**)
  und einer Liste der **abgelehnten** Bewerbungen unten
- `app/forms.py`: `ConfirmForm` (CSRF-geschütztes Ablehnen)
- Templates: `listings/detail.html` (Owner-Leiste), neue `listings/applications.html`

**Neu — Chat (`Message`):**
- `app/models.py`: Tabelle `Message` (sender/receiver/listing/body/sent_at/read_at) —
  Nachrichten werden **dauerhaft in der DB gespeichert** (lokal SQLite)
- `app/forms.py`: `MessageForm`
- `app/routes/chat.py`: `chat`-Blueprint — Inbox (Konversationen + Anzahl ungelesen) und
  Konversation (`/chat/<user_id>`); eingehende Nachrichten werden beim Öffnen als gelesen
  markiert (Gelesen/Gesendet-Anzeige)
- Templates `chat/inbox.html`, `chat/conversation.html`; „Nachricht senden" auf Profil &
  Inserent-Karte; „Chat" in der Navigation
- `app/__init__.py`: `chat_bp` registriert
- `seed.py`: 3 Beispiel-Bewerbungen + 2 Beispiel-Nachrichten

**Getestet:** Test-Client end-to-end — bewerben, Doppel-/Eigenbewerbung blockiert, Inserent
sieht Bewerber, Bewerber sieht Status; Chat: Inbox, Konversation beidseitig, Senden,
Gelesen-Status, Self-Chat → 400. DB neu geseedet (Schema-Änderung: `application`, `message`).

## Schritt 8 — Favoriten (2026-06-30)

Inserate können jetzt pro User als Favorit gespeichert und wieder entfernt werden.
Die gemerkten Inserate sind in einer eigenen Favoriten-Übersicht sichtbar.

**Neu — Favorit (`Favorite`):**
- `app/models.py`: Tabelle `Favorite` (user/listing/created_at), Unique-Constraint pro
  (User, Inserat)
- `app/routes/listings.py`: Favoriten-Liste (`/listings/favorites`) und Toggle-Route
  (`/listings/<id>/favorite`) zum Speichern/Entfernen
- `app/templates/listings/detail.html`: Stern-Button **„Als Favorit merken"** /
  **„In Favoriten"** auf der Inserat-Detailseite
- Neues Template `listings/favorites.html`: Übersicht aller gespeicherten Inserate mit
  **Entfernen**-Button

**Geändert:**
- `app/templates/base.html`: Navigationseintrag **Favoriten**
- `app/static/css/style.css`: Styling für Favoriten-Toggle und Karten-Aktionen
- `BUILD_PLAN.md`: Favoriten als erledigt markiert
- `CODEX.md`: Projektstatus und nächste Schritte aktualisiert

**Getestet:** Test-Client end-to-end — Detailseite zeigt Favoriten-Button,
POST auf `/listings/2/favorite` speichert das Inserat, `/listings/favorites` zeigt es an,
zweiter POST entfernt es wieder; DB-Count ging `0 → 1 → 0`.

## Schritt 9 — Besichtigungstermine (2026-06-30)

Interessenten können auf einer Inserat-Detailseite einen Besichtigungstermin mit
Datum und Uhrzeit anfragen. Inserenten sehen die Anfragen gesammelt und können
sie annehmen oder ablehnen; alternative Zeiten laufen bewusst über den bestehenden Chat.

**Neu — Besichtigung (`Appointment`):**
- `app/models.py`: Tabelle `Appointment` (listing/applicant/owner/scheduled_at/nachricht/status/created_at)
- `app/forms.py`: `AppointmentForm` mit `datetime-local`-Feld und optionaler Nachricht
- `app/routes/listings.py`: Route zum Senden einer Anfrage
  (`/listings/<id>/appointments/request`)
- `app/routes/listings.py`: Owner-Übersicht (`/listings/<id>/appointments`) mit offenen und
  bearbeiteten Anfragen
- `app/routes/listings.py`: Annahme/Ablehnung über
  `/listings/<id>/appointments/<appointment_id>/<decision>`
- Neues Template `listings/appointments.html`: Verwaltung der Besichtigungsanfragen

**Geändert:**
- `app/templates/listings/detail.html`: Formular **Besichtigung anfragen**, eigene
  Anfrage-Statusliste und Owner-Link **Besichtigungen (N)**
- `app/static/css/style.css`: Styling für Owner-Aktionen, Terminliste und Status-Badges
- `BUILD_PLAN.md`: Besichtigungstermin als erledigt markiert
- `CODEX.md`: Projektstatus und nächste Schritte aktualisiert

**Getestet:** Test-Client end-to-end — Anfrage über `/listings/2/appointments/request`
gesendet, Owner-Seite `/listings/2/appointments` geöffnet, Anfrage angenommen und
Status auf `angenommen` geprüft.

## Schritt 10 — E-Mail-Benachrichtigung bei Bewerbung (2026-06-30)

Inserent bekommt eine E-Mail, wenn sich jemand auf sein Inserat bewirbt — über die
**SendGrid HTTP-API** (kein SMTP, da Render-Free SMTP-Ports blockiert).

**Neu:**
- `app/email.py`: `send_email(to, subject, html, text=None)` über SendGrid (`urllib`, keine neue
  Abhängigkeit). **Ohne `SENDGRID_API_KEY`/`MAIL_FROM`** wird die Mail nur ins Log geschrieben
  (läuft lokal ohne Setup), **mit Key + verifiziertem Absender** wirklich versendet. Fehler beim
  Versand werfen nie nach oben (nur Log, inkl. HTTP-Status/Body bei API-Fehlern). Optionaler
  Klartext-Teil neben HTML (bessere Zustellbarkeit/Spam-Wertung).
- `config.py` + `.env.example`: `SENDGRID_API_KEY`, `MAIL_FROM`, `MAIL_FROM_NAME`.
- `app/routes/listings.py`: nach gespeicherter Bewerbung Mail an `listing.owner.email`.
- **Gestaltete HTML-Mail**: `app/templates/email/application_notification.html` — Tabellen-Layout
  mit Inline-Styles, FlatMate-Logo/Header in Markenfarbe, Zitatbox für die Bewerber-Nachricht
  und „Bewerbungen ansehen"-Button. Variablen werden durch Jinja escaped (kein HTML-Injection).

**Warum SendGrid:** Single Sender Verification erlaubt das Verifizieren EINER Absender-Adresse
(z. B. ein Gmail) per Bestätigungslink — ohne eigene Domain — und danach Versand an **beliebige**
Empfänger. (Resend-Testabsender liefert nur an die eigene Account-Adresse.)

**Lokal vs. deployed:** lokal ohne Key → Log-Ausgabe; auf Render `SENDGRID_API_KEY` + `MAIL_FROM`
als Env-Vars setzen → echter Versand an alle.

**Getestet:** Dev-Modus loggt Empfänger/Betreff und sendet nicht; Bewerbung wird trotzdem
gespeichert; Versandpfad mit (Fake-)Key scheitert kontrolliert (keine Exception, nur Warnung).

## Schritt 11 — E-Mail bei Besichtigungsanfrage (2026-06-30)

Analog zur Bewerbung bekommt der Inserent jetzt auch eine E-Mail, wenn jemand einen
**Besichtigungstermin** anfragt.

**Neu:**
- `app/routes/listings.py`: `request_appointment` sendet nach gespeicherter Anfrage eine Mail
  an `listing.owner.email` (mit Name, **Wunschtermin** und optionaler Nachricht).
- **Gestaltete HTML-Mail**: `app/templates/email/appointment_notification.html` — gleiches
  FlatMate-Design wie die Bewerbungs-Mail, plus hervorgehobener Wunschtermin und Button
  „Besichtigungen verwalten". Klartext-Variante für bessere Zustellbarkeit.
- Nutzt denselben `send_email()`-Helfer (Log-Fallback ohne Key, Fehler werfen nie nach oben).

**Getestet:** Template rendert mit formatiertem Datum; Anfrage-Flow loggt die Mail im Dev-Modus
und speichert die Anfrage trotzdem.

## Schritt 12 — Template-Struktur aufgeräumt (2026-06-30)

Reine Aufräumarbeit, keine Funktionsänderung.

**Geändert:**
- Profil-Templates in eigenen Ordner verschoben: `profile.html` → `profile/view.html`,
  `profile_edit.html` → `profile/edit.html` (jetzt ein Ordner pro Bereich; oberste
  Template-Ebene enthält nur noch `base.html`). Referenzen in `app/routes/profile.py` angepasst.
- Gemeinsames E-Mail-Layout `email/base_email.html` (Header/Logo + Footer); `application_`
  und `appointment_notification.html` erben davon (`{% block body %}`) — keine doppelte
  Tabellen-Struktur mehr.

**Getestet:** App-Boot; `/profile`, `/profile/edit`, `/profile/<id>` liefern 200; beide
E-Mail-Templates rendern weiterhin korrekt (Logo, Footer, CTA, Wunschtermin).

## Schritt 13 — Inserat: Validierung, Status-Wechsel & Bearbeiten (2026-06-30)

**Validierung bei Inserat erstellen:**
- `app/forms.py` `ListingForm`: `rent` mit `NumberRange` (1–100000), optionale Zahlenfelder
  (`deposit`, `room_size`, `flatmates`) als `Optional()` + `NumberRange` — leere Felder erzeugen
  keinen Fehler mehr, ungültige/negative Werte werden abgelehnt. `available_from`/`strasse` optional.

**Status-Wechsel:**
- `app/routes/listings.py` `new`: beim Erstellen eines Inserats wird `current_user.rolle` auf
  `anbietend` gesetzt — das Profil zeigt dann nicht mehr „Auf Wohnungssuche".

**Inserat bearbeiten (neu):**
- `app/routes/listings.py` `edit` (`/listings/<id>/edit`, nur Eigentümer, sonst 403): Formular
  vorbefüllt; vorhandenes Bild bleibt, wenn kein neues hochgeladen wird.
- Upload-Logik in Helper `_save_listing_photo()` ausgelagert (von `new` und `edit` genutzt).
- `new.html` → **gemeinsames `listings/form.html`** für Erstellen und Bearbeiten (Überschrift via
  `heading`, aktuelles Bild bei Bearbeiten sichtbar).
- `listings/detail.html`: Owner-Leiste hat jetzt Button **„Inserat bearbeiten"**.

**Getestet:** ungültige Eingabe (Miete 0 / Kanton leer) wird abgelehnt, kein Inserat angelegt;
gültiges Erstellen setzt `rolle=anbietend`; leere Optionalfelder ok; Bearbeiten speichert,
Nicht-Eigentümer erhält 403.

## Schritt 14 — Datenbank auf Supabase (Postgres) umgestellt (2026-06-30)

Die App kann jetzt eine gehostete **Supabase/Postgres**-DB nutzen (statt nur lokaler SQLite).
Code war dafür schon vorbereitet (`config.py` liest `DATABASE_URL`); ergänzt wurde der Treiber
und ein Schutz vor versehentlichem Überschreiben.

**Neu / geändert:**
- `requirements.txt`: **`psycopg2-binary`** (Postgres-Treiber) ergänzt — ohne ihn schlägt die
  Verbindung mit `No module named psycopg2` fehl.
- `config.py`: `SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}` — Supabase schliesst inaktive
  Verbindungen / pausiert Free-Projekte; pre_ping baut die Verbindung bei Bedarf neu auf.
- `.env.example`: Hinweis auf **Session-Pooler**-Connection-String (Port 5432, IPv4).
- `seed.py`: **`--force`-Schutz** — gegen eine externe DB (nicht-SQLite) bricht der Seeder ab,
  ausser man ruft `python seed.py --force`. Verhindert, dass die geteilte Supabase-DB
  versehentlich gelöscht/überschrieben wird.

**Setup (Kurz):** Supabase-Projekt → Settings → Database → Connection string → **Session pooler**
→ in `.env` als `DATABASE_URL` (Passwort einsetzen; Sonderzeichen URL-encoden). Einmalig mit
`python seed.py --force` befüllen. Direct-Connection (`db.<ref>.supabase.co`) ist IPv6-only →
Pooler nutzen. Free-Projekt pausiert nach ~7 Tagen Inaktivität.

**Wichtig:** `seed.py --force` löscht & überschreibt ALLE Tabellen der geteilten DB — nur bewusst
einsetzen. `DATABASE_URL`/Secrets nur via `.env` (gitignored), nie committen.

**Getestet:** Verbindung erfolgreich (PostgreSQL 17.6); Seeder mit `--force` legt Tabellen +
Dummy-Daten in Supabase an (10 User / 5 Inserate / 3 Bewerbungen / 2 Nachrichten); App-Login und
Seiten laden gegen Supabase; `--force`-Schutz bricht ohne Flag korrekt ab, ohne Daten zu ändern.
## Schritt 15 - Google Maps fuer Inserate (2026-06-30)

Inserate haben jetzt eine Kartenintegration auf der Detailseite und eine eigene Kartenansicht
fuer alle verfuegbaren Inserate.

**Neu:**
- `config.py` + `.env.example`: `GOOGLE_MAPS_API_KEY` als Konfigurationswert ergaenzt
  (`.env` bleibt lokal und wird nicht committet).
- `app/templates/listings/detail.html`: Google-Maps-Embed im Abschnitt **Lage**, basierend auf
  `strasse`, `ort`, `kanton` und `Switzerland`; ohne Key erscheint ein Google-Maps-Suchlink.
- `app/routes/listings.py`: neue Route `/listings/map`, die alle Inserate mit Adresse,
  Detail-Link und den wichtigsten Wohnungsdaten als JSON fuer die Karte vorbereitet.
- Neues Template `app/templates/listings/map.html`: Google Maps JavaScript API mit Markern fuer
  alle Inserate; Klick auf einen Marker zeigt rechts die Details des ausgewaehlten Inserats
  statt einer Gesamtliste.
- `app/templates/listings/index.html` und `app/templates/listings/map.html`: Umschalter
  **Liste / Karte** sowie fixer **Nach oben**-Button unten rechts.
- `app/static/css/style.css`: Styling fuer Karten, Marker-Detailpanel, View-Switch und
  Page-Up-Button.

**Getestet:** Syntax-/Import-Check; Test-Client-Checks fuer `/listings/`, `/listings/map` und
`/listings/1` mit Status 200 sowie Vorhandensein von Karten-Embed, View-Switch, Marker-Detailpanel
und Page-Up-Button.

## Schritt 16 - Umkreissuche fuer Inserate (2026-06-30)

Die Inserate-Uebersicht kann jetzt nach Entfernung gefiltert werden.

**Neu / geaendert:**
- `app/models.py`: `Listing` hat optionale Felder `latitude` und `longitude`.
- `app/__init__.py`: kleiner SQLite-Schema-Guard ergaenzt, damit bestehende lokale DBs die neuen
  Geo-Spalten automatisch bekommen.
- `seed.py`: Demo-Inserate enthalten Koordinaten fuer Zuerich, Basel, Bern und Winterthur.
- `app/routes/listings.py`: Umkreissuche mit `near` + `radius_km`, Geocoding-Helfer und
  Haversine-Distanzfilter. Treffer werden nach Entfernung sortiert.
- Neue/aktualisierte Inserate speichern Koordinaten, wenn die Adresse per Google Geocoding oder
  lokalem Swiss-City-Fallback aufloesbar ist.
- `app/templates/listings/index.html`: Filterfelder **Suche in der Naehe von** und **Radius**.
- `app/templates/listings/map.html`: Marker nutzen gespeicherte Koordinaten, wenn vorhanden,
  und fallen sonst auf Browser-Geocoding per Google Maps zurueck.
- `BUILD_PLAN.md`: Geo-Suche als erledigt markiert.

**Getestet:** Syntax-/Import-Check; Test-Client-Checks fuer `/listings/`,
`/listings/?near=Zuerich&radius_km=20` und `/listings/map` mit Status 200.

## Schritt 17 - Adresseingabe fuer Google Maps verbessert (2026-06-30)

Die Inserat-Erstellung/-Bearbeitung erklaert jetzt klarer, welche Adressdaten fuer Google Maps
benoetigt werden.

**Geaendert:**
- `app/templates/listings/form.html`: Adressbereich neu strukturiert in Strasse, Ort und Kanton
  mit Beispielen und Hilfetexten.
- Live-Vorschau **Google sucht nach:** zeigt die zusammengesetzte Adresse, die an Google Maps
  bzw. den Geocoding-Helfer geht.
- `app/static/css/style.css`: Styling fuer Adresshinweise und Vorschau.
- `app/routes/listings.py`: Nach Erstellen/Bearbeiten erscheint eine Warnung, wenn die Adresse
  nicht eindeutig in Koordinaten umgewandelt werden konnte.

**Getestet:** Syntax-/Import-Check; Test-Client-Checks fuer `/listings/new`, `/listings/1/edit`
und `/listings/`.

## Schritt 18 - Radiusfilter als Slider (2026-06-30)

**Geaendert:**
- `app/templates/listings/index.html`: Radius-Auswahl in der Umkreissuche ist jetzt ein Slider
  von 1 bis 100 km; Maximum wird als **100+ km** angezeigt.
- `app/routes/listings.py`: `100+ km` begrenzt die Entfernung nicht hart, sortiert aber weiter
  nach Entfernung, wenn ein Suchort eingegeben ist.
- `app/static/css/style.css`: Filterpanel kompakter gemacht; Felder und Checkboxen sitzen enger
  zusammen.

**Getestet:** Syntax-/Import-Check ohne Datenbank-Test.

## Schritt 19 - Radiusfilter nutzt Ort als Zentrum (2026-06-30)

**Geaendert:**
- `app/routes/listings.py`: Wenn ein Radius aktiv ist, wird `near` als Zentrum genutzt; falls
  `near` leer ist, wird `ort` als Zentrum genutzt. `Ort=Zuerich` + `100+ km` schliesst damit
  Orte wie Winterthur nicht mehr vorab durch den Textfilter aus.
- `app/templates/listings/index.html`: Labels angepasst zu **Ort / Radius-Zentrum** und
  **Genauer Standort**, damit klarer ist, was die Felder tun.

**Getestet:** Syntax-/Import-Check ohne Datenbank-Test.

## Schritt 20 — Umbenennung FlateMate → FlatMate (2026-07-01)

Einheitliche Schreibweise des App-Namens: **FlatMate** (vorher fälschlich "FlateMate").

**Geändert:**
- UI: Marken-/Logo-Text in der Navigation, Seitentitel, Willkommens-Flash bei der Registrierung,
  beide E-Mail-Templates.
- Code/Config: `config.py` (SQLite-Datei `flatmate.db`, `MAIL_FROM_NAME` Default `FlatMate`),
  `.env` / `.env.example`, sämtliche Docs (`README`, `BUILD_PLAN`, `CLAUDE.md`, `changelog`).
- ER-Diagramm-Datei umbenannt zu `temp_flatmate_er_diagram.html` (Referenzen in den Docs angepasst).
- Alle "FlateMate"-Vorkommen im UI/Code auf "FlatMate" geändert. Der verifizierte SendGrid-Absender
  `flatmatesendgrid@gmail.com` blieb unverändert (korrekte Schreibweise, sonst bricht der Versand).

**Getestet:** App-Boot; Navigation und Titel zeigen "FlatMate"; `MAIL_FROM_NAME=FlatMate`.

## Schritt 21 — Deployment-Vorbereitung (Render) (2026-07-01)

Die App wird für das Hosting auf **Render** (Free-Tier) vorbereitet.

**Neu / geändert:**
- `requirements.txt`: **`gunicorn`** (WSGI-Server für Produktion) ergänzt.
- `render.yaml`: Blueprint für einen Free-Web-Service (Build `pip install -r requirements.txt`,
  Start `gunicorn main:app`, Python 3.13). Secrets (`DATABASE_URL`, `SENDGRID_API_KEY`, `MAIL_FROM`,
  `GOOGLE_MAPS_API_KEY`) als `sync: false` → nur im Render-Dashboard, nicht im Repo. `SECRET_KEY`
  wird von Render generiert.
- `README.md`: Abschnitt „Deployment (Render)" mit Schritten und Hinweisen.

**Hinweise:** Free-Tier schläft nach ~15 Min Inaktivität (Kaltstart ~30–60 s). Hochgeladene Bilder
(`app/static/uploads/`) sind auf Render flüchtig (Neustart löscht sie) — dauerhafte Lösung wäre
Supabase Storage. WSGI-Einstiegspunkt ist `main:app` (`app = create_app()` in `main.py`).

**Getestet:** `main:app` ist importierbar (WSGI-Entrypoint); App bootet gegen Supabase.

## Schritt 22 - Login fuehrt direkt zu Inseraten (2026-07-01)

**Geaendert:**
- `app/routes/auth.py`: Erfolgreicher Login leitet ohne `next`-Parameter direkt zur
  Inserate-Uebersicht (`/listings/`) statt zum eigenen Profil.
- Bereits eingeloggte Nutzer, die `/login` aufrufen, landen ebenfalls direkt auf der
  Inserate-Uebersicht.

**Getestet:** Syntax-/Import-Check; Test-Client-Check fuer Login-Redirect.

## Schritt 23 - Favoriten-Tab fuer Inserenten ausblenden (2026-07-01)

**Geaendert:**
- `app/templates/base.html`: Nutzer mit eigenem Inserat sehen in der Navigation nur
  **Mein Inserat** und keinen **Favoriten**-Tab mehr.
- Nutzer ohne eigenes Inserat behalten den **Favoriten**-Tab.

**Getestet:** Syntax-/Import-Check; Test-Client-Checks fuer Navigation mit und ohne
eigenes Inserat.

## Schritt 24 - Checkbox-Filter in zwei Bloecke aufgeteilt (2026-07-01)

**Geaendert:**
- `app/templates/listings/index.html`: Die Checkbox-Filter sind jetzt in zwei Bloecke
  **Ausstattung** und **Hausregeln** aufgeteilt.
- `app/static/css/style.css`: Die Checkbox-Bloecke fuellen die restlichen Filterspalten
  und bleiben responsiv, ohne eine dritte Checkbox-Spalte zu erzeugen.

**Getestet:** Syntax-/Import-Check; Test-Client-Check fuer die Inserate-Uebersicht.

## Schritt 25 - Listing-Fotos optional in Supabase Storage speichern (2026-07-01)

**Neu / geaendert:**
- `app/storage.py`: Neuer Helper fuer Uploads in Supabase Storage per HTTP-API.
- `app/routes/listings.py`: Listing-JPEGs werden zuerst in Supabase Storage hochgeladen,
  wenn `SUPABASE_URL`, `SUPABASE_STORAGE_BUCKET` und `SUPABASE_STORAGE_KEY` gesetzt sind.
  In der Datenbank bleibt wie bisher die Bild-URL in `Listing.photo_url`.
- Ohne Storage-Konfiguration bleibt der lokale Fallback nach `app/static/uploads/listings/`
  aktiv, damit lokale Entwicklung weiter ohne Cloud-Setup funktioniert.
- `config.py`, `.env.example`, `render.yaml` und `README.md`: Storage-Konfiguration dokumentiert.

**Getestet:** Syntax-/Import-Check; Test-Client-Check fuer die Inserate-Erstellung mit
lokalem Fallback ohne Storage-Konfiguration.

## Schritt 26 — Profilbilder + Inserat-Fotos im selben Storage-Bucket (2026-07-01)

Aufbauend auf Schritt 25: **Profilbilder werden jetzt ebenfalls in Supabase Storage** gespeichert
(vorher nur Inserat-Fotos), und beide nutzen **einen gemeinsamen öffentlichen Bucket** `images`.

**Geändert:**
- `app/storage.py`: generische `upload_photo(file, stem, folder="listings")`; Ordner `listings/`
  bzw. `profiles/` im selben Bucket. `upload_listing_photo` bleibt als Wrapper erhalten.
- `app/routes/profile.py`: Profilbild-Upload nutzt zuerst Supabase Storage (`profiles/`),
  sonst lokaler Fallback.
- Bucket-Name auf **`images`** vereinheitlicht (`config.py`-Default, `render.yaml`, `.env`/`.env.example`).

**Hinweis:** `SUPABASE_URL` = reines Projekt-URL (nicht der S3-Endpoint); `SUPABASE_STORAGE_KEY`
= Service-/Secret-Key; Bucket muss **public** sein.

**Getestet:** Echter Upload über `upload_photo` in beide Ordner (`listings/`, `profiles/`) des
`images`-Buckets; öffentliche URLs liefern die Bytes zurück (HTTP 200); Testobjekte danach gelöscht.

## Schritt 27 — Foto per Upload ODER direkter Bild-URL (2026-07-01)

Bei Inserat und Profil kann das Bild jetzt **entweder hochgeladen ODER als direkte URL** angegeben
werden (z. B. Unsplash-Links wie in den Seed-Daten). So bleiben die Dummy-Inserate auf Unsplash,
und trotzdem geht Upload → Supabase Storage.

**Neu / geändert:**
- `app/forms.py`: Felder `photo_url` (ListingForm) und `foto_url` (ProfileEditForm) mit
  `Optional()` + `URL`-Validierung.
- `app/routes/listings.py` + `app/routes/profile.py`: Reihenfolge — hochgeladene Datei (→ Storage)
  hat Vorrang, sonst die eingegebene Bild-URL, sonst bleibt das bestehende Bild.
- `app/templates/listings/form.html` + `profile/edit.html`: „… oder Bild-URL"-Feld; im Profil wird
  das aktuelle Bild angezeigt.

**Getestet:** Inserat mit eingefügter URL speichert diese; ungültige URL wird abgelehnt (Bestand
bleibt); Upload hat Vorrang. (Lokale SQLite, Storage deaktiviert — keine Bucket-Writes.)
## Schritt 28 - Lifestyle-Felder im Profil ergaenzt (2026-07-01)

**Neu / geaendert:**
- `app/models.py`: `User` hat neue optionale Profilfelder fuer Hobbys, Musikgeschmack,
  Wochenend-Typ, WG-Sozialleben und Kochen.
- `app/forms.py`, `app/routes/profile.py`: Die neuen Felder koennen im Profil bearbeitet
  und gespeichert werden.
- `app/templates/profile/edit.html` und `app/templates/profile/view.html`: Lifestyle-Felder
  erscheinen im Bearbeiten-Formular und auf dem Profil.
- `app/templates/listings/detail.html`: Die Inserent-Karte zeigt die Lifestyle-Felder ebenfalls.
- `app/__init__.py`: Schema-Guard ergaenzt, damit bestehende Datenbanken die neuen
  User-Spalten automatisch erhalten.

**Getestet:** Syntax-/Import-Check; Test-Client-Checks fuer Profilbearbeitung, Profilanzeige
und Anzeige der Lifestyle-Felder auf der Inserat-Detailseite.

## Schritt 29 - Seed-Daten fuer Lifestyle-Profile und neue Listing-Attribute ergaenzt (2026-07-01)

**Geaendert:**
- `seed.py`: Alle Dummy-User haben jetzt passende Werte fuer Hobbys, Musikgeschmack,
  Wochenend-Typ, WG-Sozialleben und Kochen.
- `seed.py`: Demo-Inserate von 5 auf 10 erweitert, mit variierenden Kantonen, Adressen,
  Koordinaten, Moeblierung, Haustier-/Raucherlaubnis, Zimmergroesse, Verfuegbarkeit und
  Mitbewohner-Anzahl.

**Getestet:** Syntax-/Import-Check; Seed-Daten laufen gegen eine In-Memory-SQLite-DB durch.

## Schritt 30 — Mehr Seed-Daten (40 User / 20 Inserate) (2026-07-01)

Zum Testen und um die Filter „mit Leben zu füllen" wurde der Seed deutlich erweitert.

**Geändert:**
- `seed.py`: neben den bestehenden 10 handgepflegten Usern + 10 Inseraten werden jetzt
  **zusätzliche Datensätze generiert** — total **40 User** und **20 Inserate** (reproduzierbar
  über festen `random`-Seed). 20 User sind Inserenten (`anbietend`), 20 `suchend`.
- Streuung für die Filter: 12 verschiedene Kantone, Mieten ~550–1400 CHF, unterschiedliche
  Zimmergrössen, Verfügbarkeiten, möbliert/Haustiere/Rauchen, plus **Koordinaten** je Inserat
  (für Karte + Umkreissuche) und Lifestyle-Felder (Hobbys, Musik, Wochenend-Typ …).
- Bestehende bekannte Logins (`lena@example.com` …) und die Beispiel-Bewerbungen/-Nachrichten
  bleiben erhalten.

**Getestet:** Seed gegen lokale SQLite → 40 User / 20 Inserate; 20 anbietend / 20 suchend;
12 Kantone; alle Inserate mit Koordinaten; `lena@example.com` weiterhin vorhanden.

## Schritt 31 — Aufräumen: Build-Plan, Kommentare, einheitlicher Seed (2026-07-01)

Reine Aufräumarbeit, keine funktionalen Änderungen.

**Geändert:**
- `BUILD_PLAN.md`: **Match** aus dem Funktionsumfang entfernt (sowie der Match-Score-Hinweis).
  Bereits umgesetzte, aber noch nicht gelistete Features ergänzt/als erledigt markiert:
  Inserat **bearbeiten**, **Bild-Upload → Supabase Storage / Bild-URL**, **Supabase Postgres**
  als produktive DB und **Render-Deployment** (`render.yaml`, gunicorn). Veraltete Einleitung
  aktualisiert.
- **Lange Kommentare/Docstrings gekürzt** in `app/email.py`, `app/storage.py`, `config.py`, `seed.py`.
- `README.md` + `CLAUDE.md`: Status aktualisiert (kein „Match", SendGrid statt Resend, Favoriten/
  Besichtigungen/Karte/Umkreissuche/Supabase Storage ergänzt).
- **`seed.py` vereinheitlicht**: statt „10 handgepflegte + Generator für 30 weitere" jetzt EIN
  Ansatz — Daten-Pools + `make_user()`/`make_listing()` + eine Build-Schleife (40 User / 20 Inserate,
  fester Seed). `lena@example.com` bleibt als Demo-Login (User #0), Beispiel-Bewerbungen/-Nachrichten
  referenzieren User per Index.

**Getestet:** Seed gegen lokale SQLite → 40 User / 20 Inserate, 20 anbietend / 20 suchend,
`lena@example.com` mit Passwort und eigenem Inserat; App bootet.

## Schritt 32 — UI-Überarbeitung: Navbar, Icons, Buttons (2026-07-01)

Optischer Feinschliff des bestehenden CSS-Designsystems (kein neues Framework — Tailwind
hätte einen Node-Buildstep + Rewrite aller Templates bedeutet; das vorhandene System wurde
stattdessen aufgewertet).

**Neu / geändert:**
- `app/templates/_icons.html`: Inline-SVG-Icon-Set als Jinja-Makro `icon('name')` (Feather-Stil,
  `currentColor`, keine Abhängigkeit / offline-fähig).
- **Navigation** (`base.html`): sticky Navbar mit Marken-Icon und Icon-Links (Inserate, Karte,
  Favoriten, Chat). **Logout aus der Navbar entfernt** → neues **Profil-Dropdown** (Avatar + Name)
  mit *Mein Profil*, *Mein Inserat* (falls Inserent), *Profil bearbeiten* und *Logout*.
  Auf kleinen Screens nur Icons (Labels ausgeblendet); Dropdown schliesst bei Aussenklick.
- `style.css`: neue Design-Tokens (Schatten, Radien, `--primary-dark`), aufgewertete Buttons
  (Icon-Ausrichtung, Hover-Lift, `.btn-sm`), Karten- und Navbar-Politur.
- Icons an zentralen Buttons ergänzt (Neues Inserat, Bewerbungen/Besichtigungen/Bearbeiten,
  Nachricht senden, Profil bearbeiten).

**Fix:** „Registrieren"-Button in der Navbar war schlecht lesbar (dunkle Schrift auf Blau,
weiss beim Hover), weil `.nav-links a` die `.btn-primary`-Farben überschrieb → Nav-Link-Styles
auf `.nav-links a:not(.btn)` eingeschränkt, damit Buttons im Nav ihr Button-Styling behalten.

**Getestet:** Alle Seiten rendern (Index, Detail, Profil, Bearbeiten, Chat, Favoriten, Karte,
Bewerbungen) mit Status 200/302; Navbar mit Icons + Profil-Dropdown; Logout nur noch im Dropdown;
Registrieren-Button weiss auf Blau (lesbar).

## Schritt 33 — Nav-Badges, Doppel-Versand-Schutz, Live-Chat (Polling) (2026-07-01)

**Nav-Badges (ungelesen/offen):**
- `app/__init__.py`: Context-Processor `inject_nav_counts` liefert `nav_unread_messages`
  (ungelesene Chat-Nachrichten) und `nav_listing_activity` (offene Bewerbungen + offene
  Besichtigungen des eigenen Inserats) an alle Templates.
- `base.html`: rote Badge am **Chat**-Icon und am **Profil-Dropdown / Mein Inserat**
  (max. Anzeige „9+"). `style.css`: `.nav-badge`.

**Doppel-Versand verhindern (Chat):**
- `chat/conversation.html`: beim Absenden wird der Senden-Button gesperrt und auf „Senden…"
  gesetzt — verhindert Doppelnachrichten bei langsamem Render.

**Live-Chat via Polling:**
- `app/routes/chat.py`: JSON-Endpoint `/chat/<user_id>/messages?after=<id>` liefert neue
  Nachrichten und markiert eingehende als gelesen.
- `chat/conversation.html`: JS pollt alle 5 s und hängt neue Nachrichten an (kein Reload nötig);
  `body` via `textContent` (kein HTML-Injection).

**Hinweise/Grenzen:** Lese-Bestätigung („Gesendet"→„Gelesen") bereits angezeigter eigener
Nachrichten aktualisiert sich erst beim nächsten Seitenaufruf (Polling hängt nur neue an).
Der Context-Processor macht ~2–3 zusätzliche COUNT-Queries pro Request (auf Supabase vertretbar).

**Getestet:** Owner sieht Chat-Badge (2) + Aktivitäts-Badge (1); Poll-Endpoint gibt neue
Nachrichten zurück und markiert gelesen → Badge verschwindet; `after`-Filter; Konversation
rendert mit `data-id`, 5 s-Poll und gesperrtem Senden-Button.

## Schritt 34 — Inserat-Formular breiter & mehrspaltig (2026-07-01)

Das Formular zum Erstellen/Bearbeiten war eine schmale Ein-Spalten-Kolonne mit viel Scrollen.

**Geändert:**
- `app/templates/listings/form.html`: Felder in ein **responsives 2-Spalten-Raster** gruppiert
  (Titel/Beschreibung/Adresse/Vorschau volle Breite via `span-2`; Miete|Depot, Ort|Kanton,
  Zimmergrösse|Verfügbar ab, Mitbewohner|Ausstattung, Foto-Upload|Bild-URL nebeneinander).
- `app/static/css/style.css`: `.listing-form-card` (max. 820px), `.form-grid`, `.span-2`,
  `.form-field`; auf < 640px wieder einspaltig. Adress-Vorschau + JS unverändert.

**Getestet:** Erstellen- und Bearbeiten-Formular rendern mit Raster, allen Feldern,
Löschen-Button und Adress-Vorschau (lokale SQLite).
