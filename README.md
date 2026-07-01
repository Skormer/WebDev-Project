# 🏠 FlatMate

A flat-/roommate-matching web app built with **Python + Flask** (ZHAW Full-Stack Web
Development module). Users create a profile, browse flat listings, and get matched with
compatible flatmates. Built **step by step** — every completed feature is recorded in
[`changelog.md`](changelog.md).

## 📚 Project documentation

The agreed scope and design live in these files — read them before larger changes:

| File | What's in it |
|---|---|
| [`PROJECT_GUIDELINES.md`](PROJECT_GUIDELINES.md) | Course requirements, required vs. special features, grading, deliverables |
| [`BUILD_PLAN.md`](BUILD_PLAN.md) | Target structure, milestones, day-by-day feature order |
| [`temp_flatmate_er_diagram.html`](temp_flatmate_er_diagram.html) | ER model (open in a browser) |
| [`changelog.md`](changelog.md) | What was built in each step |

## 🛠️ Tech stack

Python 3.13 · Flask · Flask-SQLAlchemy (ORM) · Flask-Login (auth) · Flask-WTF / WTForms
(forms + CSRF) · Jinja2 templates. Database: **SQLite** for local dev, **PostgreSQL
(Supabase)** for shared/deployed use.

## 🚀 Setup & run (Windows / PowerShell)

```powershell
# 1. Create & activate the virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. (optional) configure environment
copy .env.example .env        # then fill in values; safe to skip for local dev

# 4. Create the database with sample data
python seed.py                # builds flatmate.db + 40 dummy users + 20 listings

# 5. Run the dev server
python main.py                # http://127.0.0.1:5000
```

**Test login:** `lena@example.com` / `test1234` (same password for all seeded users).

## 🗄️ Database

- **No `.env` / no `DATABASE_URL`** → the app uses a local **SQLite file** (`flatmate.db`)
  in the project root. Zero setup, runs immediately. This file is **git-ignored** — it is
  *not* pushed, so each person rebuilds it with `python seed.py`.
- **`DATABASE_URL` set in `.env`** (a Supabase Postgres URI) → the same code talks to
  that cloud database instead, shared across everyone. The `.env` file is git-ignored, so
  the connection secret never lands on GitHub. The Postgres driver `psycopg2-binary` is in
  `requirements.txt`.
- **Supabase setup**: Project → Settings → Database → Connection string → **Session pooler**
  (port 5432, IPv4 — the direct `db.<ref>.supabase.co` host is IPv6-only). Put it in `.env`
  as `DATABASE_URL` and URL-encode any special characters in the password.
- ⚠️ `python seed.py` **drops and recreates all tables**. To protect the shared DB, the seeder
  **refuses to run against a non-SQLite `DATABASE_URL` unless you pass `--force`**:
  `python seed.py --force` (use deliberately — it wipes the shared data).
- Schema changes: `db.create_all()` only creates *missing* tables, it does not migrate
  changed columns. Re-run the seeder (rebuilds) or add Flask-Migrate later.

## 🖼️ Image Uploads

For each photo you can **either upload a JPEG or paste a direct image URL** (e.g. an Unsplash
link — that's what the seed data uses). If a file is uploaded it wins; otherwise the pasted URL
is used. Uploaded files, when Supabase Storage is configured, go to one **public** bucket
(default `images`) — listing photos under `listings/`, profile pictures under `profiles/` — and
the public URL is stored in the DB (`Listing.photo_url` / `User.foto_url`). Without Storage,
uploads fall back to the local `app/static/uploads/` folder (dev-only; ephemeral on Render).

Setup: create a **public** Supabase Storage bucket named `images`, then set these env vars
locally (`.env`) and on Render. `SUPABASE_URL` is the plain project URL (not the S3 endpoint),
and `SUPABASE_STORAGE_KEY` is the **service (secret)** key:

```env
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_STORAGE_BUCKET=images
SUPABASE_STORAGE_KEY=...   # service/secret key, never the publishable key
```

## 📧 Email notifications

When someone applies to a listing, the owner gets an email — sent via the **SendGrid**
HTTP API (not SMTP, since Render's free tier blocks SMTP ports).

- **No `SENDGRID_API_KEY` / `MAIL_FROM`** (local default) → the email is just written to the
  app log, so development needs no setup.
- **Both set** (in `.env` locally, or as Render env vars) → the email is sent to anyone.

Setup (no domain needed): create a free SendGrid account → **Settings → Sender Authentication
→ Single Sender** and verify one address (e.g. a Gmail) via the confirmation link → **Settings
→ API Keys** → put the key in `SENDGRID_API_KEY` and the verified address in `MAIL_FROM`.

Sending never breaks the request: if it fails, it's logged and the application is still saved.

## 🚀 Deployment (Render, free tier)

The app runs as a normal Python web service (GitHub Pages can't host it — that's static only).
A `render.yaml` blueprint is included.

1. Push to GitHub (done).
2. On **render.com** → **New + → Blueprint** → connect this repo. Render reads `render.yaml`
   (build `pip install -r requirements.txt`, start `gunicorn main:app`).
3. Set the secret env vars (marked `sync: false`) in the Render dashboard:
   `DATABASE_URL` (Supabase Session-pooler URL), `SENDGRID_API_KEY`, `MAIL_FROM`,
   `GOOGLE_MAPS_API_KEY`, `SUPABASE_URL`, `SUPABASE_STORAGE_BUCKET` and
   `SUPABASE_STORAGE_KEY`. `SECRET_KEY` is auto-generated; `MAIL_FROM_NAME` defaults to `FlatMate`.
4. Deploy — you get a public `https://…onrender.com` URL. It redeploys on every push.

Notes:
- **Cold start**: the free tier sleeps after ~15 min idle; the first request then takes ~30–60s.
  Open the URL a minute before a demo.
- **Images**: with Supabase Storage configured, profile pictures and listing photos are durable
  (stored in the `images` bucket). Without it, uploads fall back to Render's local disk, which is
  **ephemeral** (wiped on every restart/redeploy) — so configure Storage for the deployed app.

## 📁 Structure

```
config.py                 # env config; SQLite fallback when no DATABASE_URL
main.py                   # entry point -> create_app()
seed.py                   # (re)create tables + 40 dummy users + 20 listings
app/
├── __init__.py           # app factory: extensions + blueprints
├── extensions.py         # db, login_manager
├── models.py             # User, Listing, Application, Message, Favorite, Appointment
├── forms.py              # auth, profile, listing, application, message, appointment forms
├── email.py              # send_email() via SendGrid HTTP-API (logs in dev)
├── routes/               # auth.py, profile.py, listings.py, chat.py
├── templates/            # base.html + auth/ profile/ listings/ chat/ email/ (one folder per area)
└── static/css/           # base styles + responsive listing grid
```

## ✨ Features

### Core (Grundfunktionen)
- ✅ **Register / Login / Logout** — hashed passwords (Werkzeug), sessions (Flask-Login), CSRF (Flask-WTF)
- ✅ **View profiles** — structured data (age, job, city, nationality, budget, cleanliness, smoker, pets, hobbies, music, weekend type, social level) + photo
- ✅ **Store** — everything persisted in the database (Supabase Postgres deployed, SQLite locally)
- ✅ **Search / Match** — filter listings by Kanton, Ort, max rent, min room size, availability, furnished, pets & smoking, **plus a radius (km) search**. These filters are how tenants are matched to fitting rooms.
- ✅ **Chat** — 1:1 messaging, persisted, with read receipts and live updates

### Special (Sonderfunktionen)
- ✅ **Apply to a listing** — owner sees applicants and can accept / reject
- ✅ **Visitation appointments** — request a slot; owner accepts / rejects
- ✅ **Email notifications** (SendGrid) — on application, appointment request, decision, and a welcome mail
- ✅ **Favorites** — save / remove listings + a favorites list
- ✅ **Radius search** — Haversine distance (km) around a place
- ✅ **Google Maps** — map on the detail page + a full map overview with markers
- ✅ **Image upload** — to Supabase Storage (bucket `images`) or a direct image URL

### Also included
- ✅ Create / edit / delete listings (one listing per user)
- ✅ Edit / delete own profile (with confirmation)
- ✅ Role *suchend* / *anbietend* (auto-set when you post a listing)
- ✅ Live chat via 5 s polling + *Gesendet / Gelesen* status
- ✅ Unread badges in the navigation (messages + open applications/appointments)
- ✅ Responsive UI, inline-SVG icon set, profile dropdown

## 🧱 Architecture at a glance

| Layer | Technology |
|---|---|
| Backend | Flask — app factory + blueprints (`auth` / `profile` / `listings` / `chat`) |
| ORM / DB | Flask-SQLAlchemy → SQLite (local) · **Supabase Postgres** (deployed) |
| Models | `User`, `Listing`, `Application`, `Message`, `Favorite`, `Appointment` |
| Auth | Flask-Login sessions · Werkzeug password hashing · Flask-WTF CSRF |
| Forms | WTForms with server-side validation |
| Frontend | Jinja2 templates · hand-written CSS · a little vanilla JS (no framework) |
| Images | Supabase Storage (public `images` bucket) or direct URL |
| Email | SendGrid HTTP API (Single Sender, no domain needed) |
| Maps | Google Maps Embed + JS API |
| Hosting | Render — `gunicorn`, auto-deploy from GitHub via `render.yaml` |
| Config / secrets | `.env` (git-ignored) / Render env vars |

Seed data: `python seed.py` builds **40 users / 20 listings** across 12 cantons (reproducible fixed seed).
See [`BUILD_PLAN.md`](BUILD_PLAN.md) for the roadmap and [`changelog.md`](changelog.md) for the per-step history.
