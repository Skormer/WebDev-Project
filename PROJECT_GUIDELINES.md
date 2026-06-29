# 🚀 Full Stack Web Development — Project Guidelines
**Module:** w.BA.XX.2FSWD.XX · ZHAW Institut für Wirtschaftsinformatik  
**Lecturer:** Tibor Dudas  
**Block Days:** Mon–Wed (08.02.27 – 10.02.27)  
**Submission Deadline:** Saturday after block week, before 23:59h  

---

## 📋 Project Overview

We are building a **web application from scratch** using **Python + Flask** as a group of 2–3 students. The app idea is our own — no existing projects allowed. Think of it as a Teams/WhatsApp-style communication and profile platform, but we define the scope ourselves.

> 💡 **Our App Idea:** _[TO BE DEFINED — fill in after team discussion]_

---

## 👥 Team & Roles

| Role | Profile | Member |
|---|---|---|
| Frontend | Gestalterisch | _TBD_ |
| Backend | Technisch | _TBD_ |
| Datenbank / Datenmodell | Technisch | _TBD_ |
| User Experience | Gestalterisch | _TBD_ |
| Requirements-Engineering | Gestalterisch | _TBD_ |
| Test-Engineering | Technisch | _TBD_ |

> Note: In a 2–3 person group, each member covers multiple roles.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| Web Framework | Flask |
| Database | MySQL (or SQLite for dev) |
| ORM | Flask-SQLAlchemy |
| Auth | Flask-Login |
| Forms | Flask-WTF / WTForms |
| Frontend | HTML, CSS, JS (+ optional frameworks) |
| Version Control | Git / GitHub |

---

## ✅ Required Features (Grundfunktionalitäten)

These are the **minimum** features needed to pass (grade 4.0 baseline):

- [ ] **View** — Display user profiles with structured data (age, height, hair color, etc.), free-text description, and photos
- [ ] **Store** — All data persisted in a database (MySQL)
- [ ] **Search** — Parametric search for other profiles (e.g. distance, age range)
- [ ] **Match** — Simple match algorithm based on structured data comparison
- [ ] **Chat** — 1:1 text messaging (send & receive)
- [ ] **3 Sonderfunktionen** — Three additional/special features (see below)

---

## ⭐ Optional / Special Features (Sonderfunktionalitäten)

Pick at least 3. More = better grade. Creativity welcome!

- [ ] Geo-Location / Distance calculation
- [ ] AI reply assistant (KI-Antworthilfe)
- [ ] AI coach (KI-Coach)
- [ ] Date scheduling
- [ ] Email / SMS / WhatsApp notifications (new messages, profile visits)
- [ ] Video chat
- [ ] Online status indicator
- [ ] Message read receipts (Gesendet/Gelesen)
- [ ] Auto-delete messages after X days
- [ ] Extended profile data (job, hobbies)

---

## 💎 Nice-to-Have

- Online status
- Read receipts ("sent / seen")
- Message auto-expiry after X days
- Rich profile data (profession, hobbies)

---

## 📅 3-Day Schedule & Daily Goals

### Day 1 — Foundation

| Role | Goal |
|---|---|
| Frontend | Login page + personal profile display |
| Backend | Profile query endpoint — full stack through to DB |
| Database | ER model for personal profile + 10 dummy data records |
| UX | Requirements via mutual interviews · 3 Personas/Scenarios · Paper prototype for Search/View/Chat/Match |
| RE / Testing | Support UX work |

### Day 2 — Core Features

| Role | Goal |
|---|---|
| Frontend | Search / View / Chat / Match implemented |
| Backend | Full implementation of all core features + DB controllers/entities |
| Database | Complete ER model for all core features |
| UX | Extended requirements, scenarios, and design toward special features |
| RE / Testing | Support and document |

### Day 3 — Polish & Testing

| Role | Goal |
|---|---|
| Frontend + Backend | Core + special features implemented, ready for test run |
| Database | Finalized |
| UX / Testing | Develop test procedures, execute them → produce **prioritized bug list** |

---

## 📦 Deliverables (Abgabe via Moodle)

All items must be submitted **before Saturday 23:59h**:

- [ ] **GitHub Release link** — duda/heej must be added as Contributors
- [ ] **Video demo** — recorded via Teams, max. **10 minutes**, every member must speak and present a meaningful part
- [ ] **Project diary (Tagebuch)** — Excel or PDF (template on Moodle), tracking who worked how many hours on what

---

## 🎓 Grading

| Grade | Requirement |
|---|---|
| **4.0** | All core features + 3 special features working reasonably, all 3 artefacts submitted in acceptable quality |
| **→ 6.0** | Quantity AND/OR quality of extra features + excellent UX design (both front- and backend evaluated) |

> ⚠️ No revisions allowed after submission ("Nachbesserung nicht möglich")  
> ⚠️ 100% attendance required — missing any session = module failed

---

## 🔧 Development Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_REPO_URL
cd YOUR_PROJECT

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Enable debug mode (Windows PowerShell)
$env:FLASK_DEBUG="1"

# 5. Run the app
flask --app main run
```

Visit: http://127.0.0.1:5000

---

## 📁 Project Structure (Suggested)

```
project/
├── main.py                  # App entry point
├── requirements.txt
├── README.md
├── /static
│   ├── /css
│   ├── /js
│   └── /images
├── /templates               # Jinja2 HTML templates
│   ├── base.html
│   ├── login.html
│   ├── profile.html
│   ├── search.html
│   └── chat.html
├── /models                  # SQLAlchemy models
│   ├── user.py
│   └── message.py
├── /routes                  # Flask blueprints / controllers
│   ├── auth.py
│   ├── profile.py
│   ├── search.py
│   └── chat.py
└── /docs
    ├── ER_model.png
    ├── personas.md
    └── test_procedures.md
```

---

## 📝 Artefacts to Create

- [ ] **ER Diagram** — data model for profiles, messages, matches
- [ ] **3 Personas + Scenarios** — who uses the app, what problem does it solve
- [ ] **Paper Prototype** — sketched UI for core flows
- [ ] **Test Procedures** — step-by-step test cases
- [ ] **Bug List** — prioritized from Day 3 testing
- [ ] **Project Diary** — hours per person per task

---

## 💬 Notes & Decisions

_Use this section to track important team decisions during the project._

- [ ] App idea confirmed with lecturers: **[TBD]**
- [ ] DB choice: MySQL / SQLite
- [ ] Special features selected: **[TBD]**
- [ ] GitHub repo created: **[URL here]**

---

*Last updated: [DATE] — Fill in as the project evolves*
