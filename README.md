# Career Guidance Platform

Full-stack career recommendation app using a Django REST API, React frontend, and vector-based ML matching.

## What it does

- 35-question quiz to build a user profile
- Top-5 career recommendations with match percentages and explanations
- Profile charts (abilities, work style, interests)
- Browse all careers, search, and bookmark
- Career details, roadmap, and skill-gap analysis
- Quiz history (tap history item to reopen full results + charts)

## Tech stack

- Backend: Django, Django REST Framework, Token Auth, SQLite
- Frontend: React
- ML: NumPy, cosine similarity, weighted feature vectors

## Quick start

### Automated Setup (Windows)

```powershell
.\setup.ps1    # One-time setup
.\start.ps1    # Start both servers
```

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py populate_initial_data
python manage.py runserver
```

Backend runs on `http://localhost:8000`.

**Frontend:**
```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`.

## Main API endpoints

### Public

- `GET /api/health/`
- `GET /api/info/`
- `GET /api/careers/`
- `GET /api/careers/{id}/`
- `GET /api/careers/{id}/roadmap/`

### Auth & user

- `POST /api/auth/signup/`
- `POST /api/auth/login/`
- `GET /api/auth/profile/`

### Prediction & analysis

- `POST /api/predict/`
- `GET /api/predict/history/`
- `GET /api/skill-gap/?career=<name>`
- `GET /api/learning-path/?career=<name>`

### Bookmark

- `POST /api/careers/{id}/bookmark/` with `{ "action": "add" | "remove" }`

## Documentation kept in this repo

- `README.md` (this file)
- `QUICKSTART.md` (step-by-step run guide)
- `TRANSFER.md` (how to move project to another computer)
- `QUICK_REFERENCE.txt` (command and endpoint cheat sheet)
- `BACKEND_SETUP_GUIDE.txt` (backend-focused setup and troubleshooting)
