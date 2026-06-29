# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

**FlateMate** — a Flask flat-/roommate-matching web app (ZHAW Full-Stack module project, lecturer Tibor Dudas). It's built **step by step**: each completed feature gets an entry in `changelog.md`. The agreed design lives in three docs — read them before non-trivial work:

- `BUILD_PLAN.md` — target structure, milestones, day-by-day feature order
- `PROJECT_GUIDELINES.md` — course requirements, required vs. special features, grading
- `temp_flatemate_er_diagram.html` — full ER model (7 tables) the schema grows toward
- `README.md` — project overview + setup/run instructions
- `changelog.md` — what was built per step (update it when finishing a step)

## Current state (Step 1 done)

Login + profile-from-DB only. Implemented: app factory, `User` model, register/login/logout, own + other profile views, seed. **Only the `User` table exists** so far — `Listing`, `Message`, `Favorite`, etc. from the ER diagram are added in later steps, not upfront.

## Commands (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py            # DROPS & recreates tables, inserts 10 dummy users
flask --app main run      # or: python main.py  (debug server on :5000)
```

Test login: `lena@example.com` / `test1234` (same password for all seeded users).

No test framework is set up yet; the flow was verified ad-hoc via Flask's `app.test_client()`.

## Architecture

- **App factory** in `app/__init__.py` (`create_app`) wires extensions and registers blueprints; `main.py` and `seed.py` both call it. Extensions (`db`, `login_manager`) live in `app/extensions.py` and are initialized via `init_app` to avoid circular imports.
- **Config** in `config.py` reads `.env` (via python-dotenv). `DATABASE_URL` is optional: **if unset, it falls back to a local SQLite file** (`flatemate.db`) so the app runs with zero external setup. Set `DATABASE_URL` (Supabase/Postgres) in `.env` for the real DB; `postgres://` is auto-normalized to `postgresql://`.
- **Models** in `app/models.py`. `db.create_all()` runs in the factory and creates only *missing* tables — it does **not** migrate changed columns. After a schema change, re-run `python seed.py` (drops & rebuilds) or introduce Flask-Migrate.
- **Routes** are blueprints under `app/routes/` (`auth`, `profile`). Templates in `app/templates/`, CSS in `app/static/css/`.
- **Auth**: passwords hashed with Werkzeug (`User.set_password`/`check_password`); sessions via Flask-Login. Forms use Flask-WTF — CSRF is on, so any POST test must include the token (or set `WTF_CSRF_ENABLED=False` in a test config).

## Conventions

- Domain/field names are **German** (`alter`, `beruf`, `budget_min`, `raucher`, `sauberkeit`), matching the ER diagram. Keep new model fields consistent with it.
- When finishing a feature/step, **add a `changelog.md` entry** and note any deliberate deviation from `BUILD_PLAN.md`.
- Secrets only via `.env` (gitignored), never committed.
