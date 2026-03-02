# Transfer to Another Computer

## Quick Transfer Guide

### Method 1: Using Git (Recommended)

**On current computer:**
```powershell
# Initialize repo if not already done
git init
git add .
git commit -m "Career guidance platform"

# Push to GitHub (create repo first on github.com)
git remote add origin https://github.com/yourusername/career-guidance.git
git push -u origin main
```

**On new computer:**
```powershell
# Clone the repository
git clone https://github.com/yourusername/career-guidance.git
cd career-guidance

# Run automated setup
.\setup.ps1

# Start servers
.\start.ps1
```

### Method 2: Using USB/Cloud Drive

**What to copy:**
```
ml/
├── backend/
│   ├── career_app/
│   ├── ml/
│   ├── config/
│   ├── manage.py
│   ├── requirements.txt
│   └── ... (all Python files)
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ... (all JS/JSX files)
├── setup.ps1
├── start.ps1
├── QUICKSTART.md
└── README.md
```

**DO NOT COPY:**
- `backend/.venv/` or `backend/.venv-1/` (virtual environment)
- `backend/__pycache__/` (Python cache)
- `backend/db.sqlite3` (database - will be recreated)
- `frontend/node_modules/` (npm packages - will be reinstalled)
- Any `.pyc` files

**On new computer:**
```powershell
# After copying files to new computer
cd path\to\ml

# Run automated setup
.\setup.ps1

# Start servers
.\start.ps1
```

## Manual Setup (Alternative)

If you prefer step-by-step control:

### Prerequisites
1. Install Python 3.10+ from [python.org](https://python.org)
2. Install Node.js 18+ from [nodejs.org](https://nodejs.org)

### Backend Setup
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py populate_initial_data
python manage.py createsuperuser
```

### Frontend Setup
```powershell
cd frontend
npm install
```

### Start Both Servers
Terminal 1 (Backend):
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

Terminal 2 (Frontend):
```powershell
cd frontend
npm start
```

## Verify Installation

1. Backend health check: `http://localhost:8000/api/health/`
2. Frontend: `http://localhost:3000`
3. Admin panel: `http://localhost:8000/admin/`

## Troubleshooting

**"Python not found"**
- Install Python 3.10+ and make sure it's in PATH
- Restart terminal after installation

**"Node not found"**
- Install Node.js 18+ and make sure it's in PATH
- Restart terminal after installation

**"Port already in use"**
- Backend: `python manage.py runserver 8001`
- Frontend: Set `PORT=3001` environment variable

**Database errors**
- Delete `backend/db.sqlite3`
- Run `python manage.py migrate` again
- Run `python manage.py populate_initial_data` again

## Notes

- The database will be empty on first setup (you'll create a new admin user)
- User accounts and quiz history will NOT transfer (stored in database)
- If you need to transfer data, copy the `db.sqlite3` file too

## Need Help?

See [QUICKSTART.md](QUICKSTART.md) for detailed documentation.
