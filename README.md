# 🏠 FlateMate

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
| [`temp_flatemate_er_diagram.html`](temp_flatemate_er_diagram.html) | ER model — the 7 tables the schema grows toward (open in a browser) |
| [`CLAUDE.md`](CLAUDE.md) | Architecture notes / guidance for Claude Code |
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
python seed.py                # builds flatemate.db + 10 dummy users + 5 dummy listings

# 5. Run the dev server
python main.py                # http://127.0.0.1:5000
```

**Test login:** `lena@example.com` / `test1234` (same password for all seeded users).

## 🗄️ Database

- **No `.env` / no `DATABASE_URL`** → the app uses a local **SQLite file** (`flatemate.db`)
  in the project root. Zero setup, runs immediately. This file is **git-ignored** — it is
  *not* pushed, so each person rebuilds it with `python seed.py`.
- **`DATABASE_URL` set in `.env`** (e.g. a Supabase Postgres URI) → the same code talks to
  that cloud database instead, shared across everyone. The `.env` file is git-ignored, so
  the connection secret never lands on GitHub.
- ⚠️ `python seed.py` **drops and recreates all tables**. Fine for local SQLite; be careful
  once it points at a shared database.
- Schema changes: `db.create_all()` only creates *missing* tables, it does not migrate
  changed columns. Re-run `python seed.py` (rebuilds) or add Flask-Migrate later.

## 🖼️ Image Uploads

Profile pictures and listing photos are uploaded as JPEG files and saved into
`app/static/uploads/`. The folder is ignored by Git, so uploaded images stay local to
your workspace. Listing creation uses a file upload, not a public image URL field.

## 📁 Structure

```
config.py                 # env config; SQLite fallback when no DATABASE_URL
main.py                   # entry point -> create_app()
seed.py                   # (re)create tables + 10 dummy users + 5 listings
app/
├── __init__.py           # app factory: extensions + blueprints
├── extensions.py         # db, login_manager
├── models.py             # User + Listing
├── forms.py              # auth, profile, listing forms
├── routes/               # auth.py, profile.py, listings.py
├── templates/            # base, auth/, profile, listings/
└── static/css/           # base styles + responsive listing grid
```

## ✅ Current status

**Current:** registration/login, viewing profiles, editing your own profile,
profile status (`suchend` / `anbietend`), creating/listing/detail views, the
ER model, responsive listing UI, and local JPEG uploads for profile and listing
images are implemented. Search, matching, chat and the remaining special
features follow in later steps per [`BUILD_PLAN.md`](BUILD_PLAN.md).
