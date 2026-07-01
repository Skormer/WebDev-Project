# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

**FlatMate** — a Flask flat-/roommate-matching web app (ZHAW Full-Stack module project, lecturer Tibor Dudas). It's built **step by step**: each completed feature gets an entry in `changelog.md`. The agreed design lives in three docs — read them before non-trivial work:

- `BUILD_PLAN.md` — target structure, milestones, day-by-day feature order
- `PROJECT_GUIDELINES.md` — course requirements, required vs. special features, grading
- `supabase_ER_schema.png` — ER schema exported from the Supabase schema visualizer (the live 6 tables)
- `README.md` — project overview + setup/run instructions
- `changelog.md` — what was built per step (update it when finishing a step)

## Current state

Implemented: app factory; auth; profiles (view/edit, `rolle` = `suchend`/`anbietend`, `stadt`/`nationalitaet` + lifestyle fields); listings create/edit/detail with `kanton`/`ort`/`strasse` addresses, **search filters**, a Google Maps view (`/listings/map`) and **radius (km) search**; applications (owner manages + reject) with **email on new** (SendGrid); visitation **appointments** with email on request; **favorites**; 1:1 chat with read status; **image upload → Supabase Storage** (bucket `images`) or direct URL; seed (40 users / 20 listings). **Tables: `User`, `Listing`, `Application`, `Message`, `Favorite`, `Appointment`.** DB: SQLite locally, **Supabase Postgres** deployed (Render-ready). *Match was dropped from scope.*

## Commands (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py            # DROPS & recreates tables, inserts 10 dummy users + 5 listings
python seed.py --force    # required to seed a non-SQLite DB (e.g. Supabase) — wipes shared data!
flask --app main run      # or: python main.py  (debug server on :5000)
```

Test login: `lena@example.com` / `test1234` (same password for all seeded users).

No test framework is set up yet; the flow was verified ad-hoc via Flask's `app.test_client()`.

## Architecture

- **App factory** in `app/__init__.py` (`create_app`) wires extensions and registers blueprints; `main.py` and `seed.py` both call it. Extensions (`db`, `login_manager`) live in `app/extensions.py` and are initialized via `init_app` to avoid circular imports.
- **Config** in `config.py` reads `.env` (via python-dotenv). `DATABASE_URL` is optional: **if unset, it falls back to a local SQLite file** (`flatmate.db`) so the app runs with zero external setup. Set `DATABASE_URL` (Supabase/Postgres) in `.env` for the real DB; `postgres://` is auto-normalized to `postgresql://`. Postgres driver is `psycopg2-binary`; `pool_pre_ping` keeps connections alive across Supabase idle-disconnects. Supabase: use the **Session pooler** string (port 5432, IPv4) — the direct `db.<ref>.supabase.co` host is IPv6-only.
- **Seeding a shared DB**: `seed.py` does `drop_all()`, so it refuses to run against a non-SQLite `DATABASE_URL` unless you pass `--force`. Local SQLite always seeds normally.
- **Models** in `app/models.py` (`User`, `Listing`, `Application`, `Message`). `db.create_all()` runs in the factory and creates only *missing* tables — it does **not** migrate changed columns. After a schema change, re-run `python seed.py` (drops & rebuilds) or introduce Flask-Migrate.
- **Routes** are blueprints under `app/routes/` (`auth`, `profile`, `listings`, `chat`). Templates in `app/templates/`, CSS in `app/static/css/`.
- **UI**: hand-written design system in `static/css/style.css` (CSS variables for colors/shadows/radii, `.btn` variants, cards). Reusable inline-SVG icons via a Jinja macro — `{% from "_icons.html" import icon %}` then `{{ icon('home') }}`. The navbar (in `base.html`) has icon links + a profile dropdown (`<details class="profile-menu">`) that holds Profil / Mein Inserat / edit / logout. No CSS framework (Tailwind etc.) — deliberately, to avoid a Node build step.
- **Auth**: passwords hashed with Werkzeug (`User.set_password`/`check_password`); sessions via Flask-Login. Forms use Flask-WTF — CSRF is on, so any POST test must include the token (or set `WTF_CSRF_ENABLED=False` in a test config).
- **Uploads**: profile/listing photos are saved as JPEG under `app/static/uploads/` (git-ignored, so images stay local). Listing creation uses a file upload, not a URL field.
- **Email** via `app/email.py` `send_email(to, subject, html, text=None)` (SendGrid HTTP-API, not SMTP — Render-Free blocks SMTP). Uses SendGrid Single Sender Verification (verify one `MAIL_FROM` address, no domain needed, sends to anyone). Without `SENDGRID_API_KEY`/`MAIL_FROM` it logs the mail instead of sending (local dev); with both set it sends. Sending never raises — failures are logged so app flow continues. Fires on a new application **and** on a new visitation request, each rendered from a template under `templates/email/` (`application_notification.html`, `appointment_notification.html` — table-based, inline styles; a plain-text part is passed too for deliverability).

## Conventions

- Domain/field names are **German** (`alter`, `beruf`, `budget_min`, `raucher`, `sauberkeit`), matching the ER diagram. Keep new model fields consistent with it.
- **One listing per user** (deliberate simplification): gate creation on `current_user.listings`; "Mein Inserat" links to `current_user.listings[0]`. Creating a listing sets the owner's `rolle` to `anbietend`. Create + edit (`/listings/<id>/edit`, owner-only) share `templates/listings/form.html` and the `_save_listing_photo()` helper.
- When finishing a feature/step, **add a `changelog.md` entry** and note any deliberate deviation from `BUILD_PLAN.md`.
- Secrets only via `.env` (gitignored), never committed.
