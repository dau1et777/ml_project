# Career Guidance Platform - Quick Start Guide

## 🚀 Getting Started

This guide will help you run the complete Career Guidance Platform with Django backend and React frontend.

## Prerequisites

- Python 3.8+ installed
- Node.js 14+ and npm installed
- Git (optional)

## 📁 Project Structure

```
ml/
├── backend/              # Django REST API
│   ├── career_app/      # Main app with models, views, services
│   ├── config/          # Django settings and URLs
│   ├── ml/              # ML service and recommender system
│   ├── manage.py
│   └── db.sqlite3       # Database (auto-created)
│
└── frontend/            # React application
    ├── src/
    │   ├── components/  # Quiz, Results, Profile, Career views
    │   ├── api.js       # API client
    │   └── App.jsx      # Main app with routing
    └── package.json
```

## 🔧 Backend Setup

### 1. Install Python Dependencies

```powershell
cd backend
pip install django djangorestframework django-cors-headers numpy
```

### 2. Apply Database Migrations

```powershell
python manage.py migrate
```

### 3. Create Admin User (Optional)

```powershell
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123 (or your choice)
```

### 4. Populate Initial Data

```powershell
python manage.py populate_initial_data
```

This command will create:
- 35 quiz questions
- 80+ career profiles
- 37 skills
- Career-skill relationships
- Sample roadmaps

### 5. Start Backend Server

```powershell
python manage.py runserver
```

Backend will run at: **http://localhost:8000**

### 6. Verify Backend Health

Open http://localhost:8000/api/health/ in your browser. You should see:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🎨 Frontend Setup

### 1. Install Node Dependencies

```powershell
cd frontend
npm install
```

### 2. Configure API URL (Optional)

Create `frontend/.env` file:
```
REACT_APP_API_URL=http://localhost:8000/api
```

### 3. Start React Development Server

```powershell
npm start
```

Frontend will run at: **http://localhost:3000**

## 🎯 Using the Application

### First Time Users

1. **Navigate to** http://localhost:3000
2. **Sign Up**: Click "Sign Up" and create an account
   - Email: your@email.com
   - Username: your_username
   - Password: minimum 8 characters
3. **Login**: Use your credentials to log in
4. **Take Quiz**: Click "Take Quiz" and answer all 35 questions
5. **View Results**: See your top 5 career recommendations with match scores
6. **Browse Careers**: Explore all available careers
7. **View Profile**: Check your quiz history and logout

### Navigation

After logging in, you'll see 3 main tabs:

- **Take Quiz** - Answer 35 questions to get career recommendations
- **Browse Careers** - Explore all career profiles
- **Profile** - View your account and quiz history

### Features

#### 1. Career Recommendations
- Answer 35 questions about your:
  - Problem-solving abilities (Q1-Q20)
  - Work environment preferences (Q21-Q25)
  - Interest areas (Q26-Q33)
  - Work style (Q34-Q35)
- Get top 5 career matches with explanations
- View match percentage for each career

#### 2. Career Details
- Click any career to see:
  - Full description
  - Salary range
  - Demand level
  - Required skills
  - Learning roadmap

#### 3. Skill Gap Analysis
- Click "Analyze Skill Gap" on any career
- See which skills you:
  - ✅ Already have (matching)
  - 🟡 Need to improve (developing)
  - 🔴 Need to learn (missing)
- Get prioritized learning recommendations

#### 4. Profile & History
- View all your past quiz results
- Track your career exploration journey
- Logout functionality

## 🔌 API Endpoints

### Public Endpoints (No Authentication)

- `GET /api/health/` - System health check
- `GET /api/info/` - API version and stats
- `GET /api/careers/` - List all careers (paginated)
- `GET /api/careers/{id}/` - Get career details
- `GET /api/careers/{id}/roadmap/` - Get career learning roadmap
- `POST /api/auth/signup/` - Create new account
- `POST /api/auth/login/` - Login and get token

### Protected Endpoints (Requires Token)

- `GET /api/auth/profile/` - Get user profile
- `POST /api/predict/` - Get career recommendations
- `GET /api/predictions/history/` - View past results
- `POST /api/careers/{id}/bookmark/` - Bookmark a career
- `POST /api/skill-gap/` - Analyze skill gap for a career
- `POST /api/learning-path/` - Get personalized learning path

### Authentication

All protected endpoints require an `Authorization` header:
```
Authorization: Token your_token_here
```

The token is automatically stored in localStorage by the frontend after login.

## 🛠️ Admin Panel

Access Django admin at: http://localhost:8000/admin/

Login with the superuser credentials you created.

You can:
- View all users and their quiz results
- Manage careers, skills, and roadmaps
- Edit quiz questions
- View bookmarks and user history

## 📊 Database Schema

### Core Models

1. **QuizQuestion** - 35 questions with types (scale/choice)
2. **Career** - 80+ career profiles with salary, demand, category
3. **Skill** - Technical, soft, and domain skills
4. **CareerSkill** - Skills required for each career
5. **UserResult** - User quiz results with top 5 careers
6. **QuizAnswer** - Individual user answers
7. **Bookmark** - User-saved careers
8. **CareerRoadmap** - Learning pathways by stage
9. **UserSkill** - User's skill proficiency (future use)

## 🔍 Troubleshooting

### Backend Issues

**Problem: Port 8000 already in use**
```powershell
# Find process on port 8000
Get-NetTCPConnection -LocalPort 8000

# Kill it (replace PID with actual value)
Stop-Process -Id PID -Force
```

**Problem: Migration errors**
```powershell
cd backend
python manage.py migrate --fake-initial
```

**Problem: Import errors**
```powershell
pip install --upgrade django djangorestframework django-cors-headers numpy
```

### Frontend Issues

**Problem: Node modules missing**
```powershell
cd frontend
rm -rf node_modules
npm install
```

**Problem: CORS errors**
- Ensure backend is running
- Check that `CORS_ALLOWED_ORIGINS` in `backend/config/settings.py` includes `http://localhost:3000`

**Problem: API connection failed**
- Verify backend is running at http://localhost:8000
- Check `.env` file has correct API URL
- Open browser console for detailed error messages

### Common Issues

**Problem: "All questions not answered" error**
- Scroll through all questions
- Ensure every question has an answer
- Questions with no selection will block submission

**Problem: Login/Signup not working**
- Check backend console for errors
- Verify database migrations are applied
- Clear browser localStorage and try again

## 📈 Testing the System

### 1. Test Backend API

```powershell
# Health check
curl http://localhost:8000/api/health/

# Get all careers
curl http://localhost:8000/api/careers/

# Signup
curl -X POST http://localhost:8000/api/auth/signup/ -H "Content-Type: application/json" -d "{\"email\":\"test@test.com\",\"username\":\"testuser\",\"password\":\"test1234\"}"
```

### 2. Test Frontend

1. Open http://localhost:3000
2. Open browser DevTools (F12)
3. Watch Network tab for API calls
4. Watch Console for any errors

### 3. End-to-End Flow

1. Sign up → Should create account and auto-login
2. Take quiz → Should show 35 questions with progress bar
3. Submit quiz → Should show 5 career recommendations
4. Browse careers → Should show paginated list
5. Click career → Should show details, skills, roadmap
6. Analyze skills → Should show skill gap analysis
7. View profile → Should show quiz history
8. Logout → Should return to login screen

## 🚀 Next Steps

### Enhancements You Can Add

1. **User Skills Management**: Allow users to add their current skills
2. **Career Comparison**: Compare 2-3 careers side by side
3. **Filters & Search**: Filter careers by salary, demand, category
4. **Bookmarks Page**: Dedicated page for saved careers
5. **Progress Tracking**: Track skill development over time
6. **Social Sharing**: Share results with friends/mentors
7. **PDF Export**: Export recommendations as PDF report

### Production Deployment

For production deployment (when ready):
1. Set `DEBUG = False` in Django settings
2. Configure proper database (PostgreSQL recommended)
3. Set up environment variables for secrets
4. Use production WSGI server (Gunicorn)
5. Build React for production: `npm run build`
6. Serve React build with Django or separate CDN
7. Configure proper CORS origins
8. Set up HTTPS/SSL certificates

## 📝 Development Guidelines

### Adding New Features

1. **Backend**: 
   - Add models in `career_app/models.py`
   - Create serializers in `career_app/serializers.py`
   - Add views in `career_app/views.py`
   - Register URLs in `career_app/urls.py`
   - Run migrations: `python manage.py makemigrations && python manage.py migrate`

2. **Frontend**:
   - Create component in `frontend/src/`
   - Add API method in `frontend/src/api.js`
   - Import and use in `App.jsx` or other components
   - Add styles in corresponding `.css` file

### Code Organization

- **Services**: Business logic goes in `career_app/services.py`
- **ML Code**: ML-related code in `backend/ml/`
- **API Client**: All backend calls through `frontend/src/api.js`
- **Components**: Keep components focused and reusable

## 💡 Tips

1. **Keep both servers running**: Backend (port 8000) and Frontend (port 3000)
2. **Check logs**: Both terminals show helpful error messages
3. **Clear cache**: If seeing old data, clear browser cache or localStorage
4. **Admin panel**: Great for debugging and manual data management
5. **Network tab**: Best way to debug API issues

## 📞 Support

If you encounter issues:
1. Check this guide's Troubleshooting section
2. Review terminal logs for error messages
3. Check browser console for frontend errors
4. Verify all dependencies are installed
5. Ensure migrations are applied

## 🎉 Success Checklist

- [ ] Backend running at http://localhost:8000
- [ ] Frontend running at http://localhost:3000
- [ ] Health endpoint returns "healthy"
- [ ] Can signup and login
- [ ] Can take quiz and see recommendations
- [ ] Can browse careers
- [ ] Can view career details
- [ ] Can see skill gap analysis
- [ ] Can view profile and history
- [ ] Can logout successfully

Once all items are checked, you're ready to use the Career Guidance Platform! 🚀
