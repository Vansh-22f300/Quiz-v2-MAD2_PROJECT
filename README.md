# QuizMaster — MAD II Project

A full-stack **multi-user quiz application** with a **Flask REST API** backend and a **Vue 3 + Vite** single-page frontend. Admins create subjects, chapters, quizzes and questions; users attempt timed quizzes, get instant scores, and track their performance with charts.

> **Live demo:** https://quiz-app-v2-py9b.onrender.com/
> Hosted on Render's free tier — the first request after idle may take ~30–60s to wake the server.

---

## 🔑 Admin Login

Default administrator account, seeded automatically on first startup (`admin_setup()` in `app.py`):

| Field    | Value   |
|----------|---------|
| Username | `admin` |
| Password | `vm123` |

Log in at **`/login`** with the credentials above to reach the admin dashboard.

> ⚠️ These are default seed credentials committed for evaluation/demo purposes. **Change them before any production use** (edit `admin_setup()` in `app.py` or update the record in the database).

New end-users can self-register from the **Sign Up** page and get a normal (non-admin) account.

---

## ✨ Features

**Admin**
- Manage subjects, chapters, quizzes and questions (full CRUD)
- Activate/deactivate quizzes, set time limits and single-attempt rules
- View all registered users
- Summary dashboard with charts (Chart.js) and data export

**User**
- Register / log in (JWT-based auth)
- Browse available quizzes and attempt them with a live countdown timer
- Instant scoring with per-question review
- Personal results history

**Platform**
- Responsive UI (mobile → desktop) built on Bootstrap 5
- Redis-backed caching (Flask-Caching)
- Email via Flask-Mail; background jobs via Celery
- `/health` endpoint for uptime monitoring

---

## 🧱 Tech Stack

| Layer       | Technology |
|-------------|------------|
| Frontend    | Vue 3, Vite 7, Vue Router 4, Bootstrap 5.3 (CDN), Chart.js + vue-chartjs |
| Backend     | Flask 3, Flask-RESTful, Flask-JWT-Extended, Flask-SQLAlchemy, Flask-Caching, Flask-Mail |
| Auth        | JWT (Flask-JWT-Extended), bcrypt / passlib password hashing |
| Database    | SQLite (local) / PostgreSQL (production) |
| Cache/Queue | Redis + Celery |
| Server      | Gunicorn (production) |
| Hosting     | Render |

---

## 📁 Project Structure

```
Quiz-v2-MAD2_PROJECT/
├── app.py                  # Flask app factory, route registration, admin seed, /health
├── requirements.txt        # Python dependencies
├── backend/
│   ├── api.py              # REST resources (login, CRUD, quiz, results, summary)
│   ├── models.py          # Models: User, Subject, Chapter, Quiz, Question, Score
│   ├── config.py          # LocalConfig / ProductionConfig
│   ├── task.py            # Celery tasks
│   ├── worker.py          # Celery worker entrypoint
│   ├── wsgi.py            # Gunicorn entrypoint
│   └── build.sh           # Builds the frontend, copies dist into backend/static
└── frontend/
    ├── src/
    │   ├── components/    # Vue views (Admin, User, Manage_*, Start_Quiz, ...)
    │   ├── router/        # Vue Router route table
    │   ├── assets/css/main.css   # App theme + responsive rules
    │   └── main.js        # App bootstrap
    └── package.json
```

---

## 🗃️ Data Model

- **User** — account (admin flag, profile, status) → has many **Score**
- **Subject** → has many **Chapter**
- **Chapter** → has many **Quiz** and **Question**
- **Quiz** — title, time limit, active flag, single-attempt → has many **Question** / **Score**
- **Question** — statement, 4 options, correct answer
- **Score** — a user's attempt: marks, percentage, grade, timestamp

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11+ and `pip`
- Node.js 18+ and `npm`
- Redis (for caching; optional for a quick run)

### 1. Backend

```bash
# from the project root
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The API starts on **http://localhost:5000** with a local SQLite database (`local.db`) and seeds the admin account on first run.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite serves the SPA on **http://localhost:5173**.

### 3. Optional services

```bash
redis-server
celery -A app.celery worker --loglevel=info --pool=solo
celery -A app.celery beat --loglevel=info
```

> **Note:** The Vue components call the deployed Render URL (`https://quiz-app-v2-py9b.onrender.com`) directly. To develop fully against a local backend, update those `fetch(...)` base URLs in `frontend/src/components/*.vue`.

---

## 🔧 Environment Variables (production)

Set these on the host (e.g. the Render dashboard):

| Variable | Purpose |
|----------|---------|
| `FLASK_ENV` | Set to `production` to load `ProductionConfig` |
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string |
| `JWT_SECRET_KEY` | Secret for signing JWTs |
| `SECURITY_PASSWORD_SALT` | Password salt |
| `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS` | SMTP settings |
| `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_SENDER` | SMTP credentials / sender |

---

## 🏗️ Build & Deploy (Render)

The production build compiles the Vue SPA and serves it from Flask as a single service:

```bash
# backend/build.sh
cd ../frontend && npm install && npm run build
cp -r dist/* ../backend/static/
```

Flask (`app.py`) serves the built frontend statically and falls back to `index.html` for client-side routes.

---

## ⏰ Keeping the App Awake

Render's free tier sleeps after **15 minutes** of no inbound traffic. A lightweight, DB-free **`/health`** endpoint returns `{"status": "ok"}` for external monitors to ping.

Two independent keep-alive mechanisms:

1. **UptimeRobot** (primary) — an HTTP(s) monitor hits `/health` every few minutes.
2. **GitHub Actions** (backup) — `.github/workflows/keep-alive.yml` pings `/health` on a `*/5` cron. Activates automatically once merged to the default branch; no secrets or manual setup required.

> Keeping a single service awake ≈ 720–744 hours/month, within Render's free 750 instance-hours.

---

## 🔌 Key API Endpoints

| Method(s) | Path | Description |
|-----------|------|-------------|
| POST | `/login`, `/signup` | Authentication |
| GET/POST/PUT/DELETE | `/add_subject/*`, `/edit_subject/<id>`, `/delete_subject/<id>` | Subjects |
| GET/POST/PUT/DELETE | `/add_chapter/*`, `/edit_chapter/<id>`, `/delete_chapter/<id>` | Chapters |
| GET/POST/PUT/DELETE | `/add_quiz`, `/edit_quiz/<id>`, `/delete_quiz/<id>`, `/get_quiz` | Quizzes |
| GET/POST/PUT/DELETE | `/add_question/<quiz_id>`, `/edit_question/<id>`, `/delete_question/<id>`, `/get_questions/<quiz_id>` | Questions |
| GET | `/start_quiz/<quiz_id>` | Load a quiz to attempt |
| GET | `/user_results` | A user's score history |
| GET | `/admin_summary`, `/admin_users` | Admin dashboards |
| GET | `/admin/profile`, `/user/profile` | Profiles |
| GET | `/export_details` | Export data |
| GET | `/health` | Uptime check (no auth, no DB) |

Protected routes require an `Authorization: Bearer <token>` header (JWT issued at login).

---

## 📱 Frontend Routes

`/` (landing) · `/login` · `/signup` · `/admin` · `/manage_subject` · `/add_chapter/:subject_id` · `/manage_quiz` · `/admin_user` · `/admin_summary` · `/user` · `/start_quiz/:quiz_id` · `/user_results`

