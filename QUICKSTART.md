# Career Guidance Platform - Quickstart

## Prerequisites

- Python 3.10+
- Node.js 18+

## Backend

```powershell
cd backend
python manage.py migrate
python manage.py populate_initial_data
python manage.py createsuperuser
python manage.py runserver
```

Backend URL: `http://localhost:8000`

Health check:

```powershell
curl http://localhost:8000/api/health/
```

## Frontend

```powershell
cd frontend
npm install
npm start
```

Frontend URL: `http://localhost:3000`

Optional env file (`frontend/.env`):

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## Basic user flow

1. Sign up / log in
2. Take the 35-question quiz
3. Review top-5 recommendations + charts
4. Browse careers and open details/roadmaps
5. Open Profile → tap a history item to reopen full results + charts

## Important routes

- `POST /api/predict/`
- `GET /api/predict/history/`
- `GET /api/careers/`
- `GET /api/careers/{id}/roadmap/`
- `GET /api/skill-gap/?career=<name>`

## Troubleshooting

- `OperationalError: no such table` → run `python manage.py migrate`
- Auth errors on protected routes → send `Authorization: Token <token>`
- Port busy → `python manage.py runserver 8001`
