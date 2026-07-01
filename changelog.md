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

## Schritt 15 — Umbenennung FlateMate → FlatMate (2026-07-01)

Einheitliche Schreibweise des App-Namens: **FlatMate** (vorher „FlateMate").

**Geändert:**
- UI: Marken-/Logo-Text in der Navigation, Seitentitel, Willkommens-Flash bei der Registrierung,
  beide E-Mail-Templates.
- Code/Config: `config.py` (SQLite-Datei `flatmate.db`, `MAIL_FROM_NAME` Default `FlatMate`),
  `.env` / `.env.example`, sämtliche Docs (`README`, `BUILD_PLAN`, `CLAUDE.md`, `changelog`).
- Datei umbenannt: `temp_flatemate_er_diagram.html` → `temp_flatmate_er_diagram.html`
  (Referenzen in den Docs mit angepasst).
- 23 Textdateien angepasst; keine „flatemate"-Vorkommen mehr. Der verifizierte SendGrid-Absender
  `flatmatesendgrid@gmail.com` blieb unverändert (korrekte Schreibweise, sonst bricht der Versand).

**Getestet:** App-Boot; Navigation zeigt „FlatMate", kein „FlateMate" mehr; `MAIL_FROM_NAME=FlatMate`.
