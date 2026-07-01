# Codex Project Notes

Read this first when returning to the project.

## Project

FlateMate is a Flask flat-/roommate-matching app for the ZHAW Full-Stack Web
Development module. Users register/login, maintain a profile, browse flat
listings, apply to listings, and chat 1:1 with other users.

## Current Code State

- App entry: `main.py` -> `app.create_app()`.
- App factory: `app/__init__.py`, with `auth`, `profile`, `listings`, and `chat`
  blueprints.
- Database: Flask-SQLAlchemy with SQLite fallback in `flatemate.db`; optional
  `DATABASE_URL` via `.env` for Postgres/Supabase.
- Implemented models in `app/models.py`: `User`, `Listing`, `Application`,
  `Favorite`, `Appointment`, `Message`.
- Implemented user flows:
  - register/login/logout
  - own/foreign profile view
  - profile edit
  - profile status: `suchend` / `anbietend`
  - JPEG profile upload to `app/static/uploads/`
  - listing overview, detail, creation, and JPEG listing photo upload
  - one listing per user
  - search filters for canton, city, max rent, min room size, availability,
    pets, and smoking
  - application flow with applicant status display and owner reject action
  - favorites: save/remove listings and view all saved apartments
  - viewing appointments: request a date/time, owner accepts or rejects
  - 1:1 chat with persisted messages, inbox, unread counts, and read status
- Seed data: `seed.py` rebuilds the DB with 10 dummy users, 5 listings,
  3 applications, and 2 messages.
- Test login: `lena@example.com` / `test1234`.

## Main Files

- `README.md`: setup, run flow, project overview
- `BUILD_PLAN.md`: milestones and planned features
- `PROJECT_GUIDELINES.md`: course requirements and grading context
- `changelog.md`: completed-step notes
- `temp_flatemate_er_diagram.html`: ER diagram target with 7 tables
- `seed.py`: destructive local DB rebuild with sample data

## Run Flow

```powershell
.\.venv\Scripts\Activate.ps1
python seed.py
python main.py
```

App runs at `http://127.0.0.1:5000`.

## Verification

Useful quick checks:

```powershell
.\.venv\Scripts\python.exe -m compileall app main.py seed.py
.\.venv\Scripts\python.exe seed.py
```

For route checks, use Flask's test client with CSRF disabled and login as
`lena@example.com` / `test1234`.

## Next Likely Work

1. Add a simple weighted `match_score()` based on budget and lifestyle, then
   sort listing results by compatibility.
2. Add email notification for new applications via an HTTP API such as Resend
   or SendGrid, not SMTP.
3. Add geo search with Haversine distance and optionally a Leaflet map.
4. Run and document test procedures, then create a prioritized bug list.
5. Prepare Render deployment settings and final submission artifacts.

## Notes For Future Edits

- Do not commit `.env`, `flatemate.db`, `__pycache__/`, or uploaded images.
- `python seed.py` calls `drop_all()`, so it deletes current DB data.
- `db.create_all()` creates missing tables only; it does not migrate changed
  columns.
- After every completed feature or schema/UI change, update `changelog.md` in
  the same turn.
- Add new changelog entries at the bottom after the latest step, not at the top.
  Keep chronological `Schritt N` order and follow the existing format: short
  summary, sections such as `Neu`, `Geändert`, and `Getestet`.
- Keep UI text in German unless the user asks otherwise.
- German UI text should use real umlauts such as `ö`, `ä`, `ü`, `Ä`, `Ö`, `Ü`
  and `ß`. Do not replace them with `oe`/`ae`/`ue` unless the user asks for
  ASCII.
- Some PowerShell output may display German/emoji strings as mojibake. Check the
  actual file encoding before broad text rewrites.
- `BUILD_PLAN.md` and `workspace-summary.md` may be stale. Prefer the current
  code, `README.md`, and `changelog.md` when they disagree.
