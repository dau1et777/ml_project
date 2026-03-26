# 🏗️ ARCHITECTURE DOCUMENT - Career Recommendation System

## Table of Contents
1. [System Overview](#system-overview)
2. [Technology Stack](#technology-stack)
3. [Database Schema](#database-schema)
4. [Backend Architecture](#backend-architecture)
5. [Frontend Architecture](#frontend-architecture)
6. [ML Algorithm Details](#ml-algorithm-details)
7. [API Specification](#api-specification)
8. [Data Flow](#data-flow)
9. [Authentication & Authorization](#authentication--authorization)
10. [Performance & Scalability](#performance--scalability)

---

## System Overview

### Core Mission
Transform 35 quiz answers into **actionable career recommendations** using **vector-based matching** with **explainable similarity scores**. Provide comprehensive career exploration with skill gap analysis, learning pathways, and personalized career bookmarking.

### Key Principles
- **Simplicity**: No black-box neural networks, pure vector math
- **Interpretability**: Users understand WHY each career matches
- **Persistence**: Save quiz results and user progress in database
- **Personalization**: Track user bookmarks and skill profiles
- **Scalability**: 130+ careers, extensible to 1000+
- **Performance**: <500ms recommendation generation

### Users
- **Unauthenticated visitors**: Take quiz, browse careers, view roadmaps
- **Registered users**: Save quiz results, bookmark careers, track skills, view history

---

## Technology Stack

### Backend
- **Framework**: Django 4.2 + Django REST Framework
- **Database**: SQLite3 (9 models, full ORM support)
- **Authentication**: Token-based (django.contrib.authtoken)
- **Serialization**: DRF Serializers with validation
- **ML**: NumPy (vector math, cosine similarity)
- **CORS**: django-cors-headers for frontend communication

### Frontend
- **Framework**: React 18 + StateManagement with hooks
- **Build**: Create React App (npm)
- **Styling**: Vanilla CSS (global + component-scoped)
- **Communication**: Fetch API + custom API service wrapper
- **State**: React hooks (useState, useEffect, useContext)
- **Routing**: Tab-based navigation (Quiz, Browse, Profile)

### Deployment
- **Web Server**: Django runserver (dev), Gunicorn + Nginx (prod)
- **Static Files**: Collected to `/staticfiles/` for admin CSS
- **CORS Settings**: Allow localhost:3000 and localhost:8000

---

## Database Schema

### Core Models

#### User (Django Built-in)
```
id, username, email, password, first_name, last_name
is_active, is_staff, date_joined
```

#### QuizQuestion
```
id (UUID)
text: TextField
question_type: Char(scale|choice)
options: JSON (for multiple choice)
category: Char(cognitive|motivation|interests|preferences)
weight: Float(default=1.0)
order: Integer
created_at, updated_at
```
- 35 questions total
- Q1-Q20: Likert scale (1-10)
- Q21-Q35: Multiple choice (A/B/C/D)

#### QuizAnswer
```
id (UUID)
user: ForeignKey(User)
question: ForeignKey(QuizQuestion)
answer_value: Char (A/B/C/D or 1-10)
answered_at: DateTime
```
- Stores user's individual question responses
- Unique constraint: (user, question)

#### Career
```
id (UUID)
name: Char(255, unique)
description: TextField
category: Char(technology|healthcare|business|engineering|creative|education|science|finance|marketing)
salary_min, salary_max: Float
demand_level: Char(high|medium|low)
created_at, updated_at
```
- **130+ careers** in system
- Synced from ML system via `sync_careers.py`
- Categories auto-assigned based on name keywords

#### CareerRoadmap
```
id (UUID)
career: ForeignKey(Career)
stage: Integer(1=Entry|2=Mid|3=Senior)
duration_months: Integer
description: TextField
skills_to_learn: JSON
created_at
```
- Learning pathway with 3 career stages
- Defines skills and time needed at each level

#### Skill
```
id (UUID)
name: Char(255, unique)
category: Char(technical|soft|domain)
description: TextField
```
- Global skill glossary
- Can be required for careers or owned by users

#### CareerSkill
```
id (UUID)
career: ForeignKey(Career)
skill: ForeignKey(Skill)
proficiency_level: Char(beginner|intermediate|expert)
```
- Links careers to required skills
- Tracks proficiency level needed

#### UserSkill
```
id (UUID)
user: ForeignKey(User)
skill: ForeignKey(Skill)
proficiency_level: Char(beginner|intermediate|expert)
years_experience: Float
```
- User's personal skill inventory
- Used for skill gap analysis

#### UserResult
```
id (UUID)
user: ForeignKey(User)
quiz_session_id: Char(unique)
top_career_1..5: Char + score_1..5: Float
explanation: JSON
top_careers_snapshot: JSON (full prediction data)
profile_snapshot: JSON (chart data)
model_version: Char
created_at
```
- Saves complete quiz results to database
- Allows users to view past results
- Stores both top 5 careers and full prediction metadata

#### Bookmark
```
id (UUID)
user: ForeignKey(User)
career: ForeignKey(Career)
created_at
```
- User's saved favorite careers
- Unique constraint: (user, career)

---

## Backend Architecture

### Directory Structure

```
backend/
├── manage.py                  [Django CLI]
├── settings.py                [Django configuration]
├── config/
│   ├── __init__.py
│   ├── wsgi.py               [WSGI application]
│   ├── asgi.py               [ASGI application]
│   └── urls.py               [Root URL routing]
│
├── career_app/                [Main Django app]
│   ├── models.py              [9 model classes]
│   ├── views.py               [18 API endpoints]
│   ├── urls.py                [URL routing for /api/]
│   ├── serializers.py         [DRF serializers with validation]
│   ├── services.py            [Business logic layer]
│   ├── signals.py             [Initial data population]
│   ├── admin.py               [Django admin configuration]
│   ├── apps.py
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_add_models.py
│   │   └── ...
│   └── management/
│       └── commands/
│           └── populate_initial_data.py  [CLI to seed database]
│
├── ml/                        [ML recommendation engine]
│   ├── __init__.py
│   ├── careers.py             [130 career vectors, similarity]
│   ├── validator.py           [Answer validation]
│   ├── vectorizer.py          [Quiz → 80-dim vector]
│   ├── weights.py             [Feature weighting]
│   ├── similarity.py          [Cosine similarity calculation]
│   ├── recommender.py         [Main orchestrator]
│   ├── ml_service.py          [Service layer wrapper]
│   └── debug.py               [Debugging utilities]
│
├── sync_careers.py            [Script to sync ML→DB careers]
├── fix_categories.py          [Script to categorize careers]
├── staticfiles/               [Collected static files for admin]
├── requirements.txt           [Python dependencies]
└── db.sqlite3                 [SQLite database]
```

### Key Components

#### views.py (18 endpoints)
```
Authentication:
  - signup(request)
  - login(request)
  - profile(request)

Predictions:
  - predict(request)
  - prediction_history(request)

Careers (ViewSet):
  - list(self, request)
  - retrieve(self, request, pk=None)
  - roadmap(self, request, pk=None)
  - bookmark(self, request, pk=None)

Analysis:
  - skill_gap_analysis(request)
  - learning_recommendations(request)

System:
  - health(request)
  - info(request)
```

#### services.py (Business Logic)
```
PredictionService:
  - predict_and_save(user, answers)
  - get_user_results(user, limit=10)
  
SkillGapService:
  - analyze(user, career_name)
  - get_missing_skills(user, career)
  
UserService:
  - create_user(email, username, password)
  - authenticate_user(email, password)
  - get_or_create_token(user)
```

#### serializers.py
```
SignupSerializer:
  - email, username, password validation

LoginSerializer:
  - email, password validation

CareerSerializer:
  - List view (name, category, demand_level)

CareerDetailSerializer:
  - Full career details + roadmap + skills

PredictionRequestSerializer:
  - Quiz answers validation

UserResultSerializer:
  - Serializes saved results with charts

UserProfileSerializer:
  - User info + skills + bookmarks
```

---

## Frontend Architecture

### Directory Structure

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── index.js               [React entry point]
│   ├── index.css              [Global styles]
│   │
│   ├── api.js                 [API service wrapper]
│   │
│   ├── App.jsx                [Root component with tabs]
│   ├── App.css
│   │
│   ├── Login.jsx              [Login form]
│   ├── Auth.css
│   │
│   ├── Signup.jsx             [Registration form]
│   │
│   ├── QuizWizard.jsx         [Quiz interface]
│   ├── QuizWizard.css
│   ├── ProgressBar.jsx        [Progress tracking]
│   ├── ProgressBar.css
│   ├── Results.jsx            [Quiz results display]
│   ├── Results.css
│   │
│   ├── CareerList.jsx         [Browse careers]
│   ├── CareerList.css
│   ├── CareerDetail.jsx       [Career detail modal]
│   ├── CareerDetail.css
│   │
│   ├── Profile.jsx            [User profile]
│   ├── Profile.css
│   │
│   ├── SkillGap.jsx           [Skill gap analysis]
│   ├── SkillGap.css
│   │
│   ├── AbilitiesChart.jsx     [Chart component]
│   ├── InterestChart.jsx      [Chart component]
│   ├── WorkStyleChart.jsx     [Chart component]
│   │
│   └── package.json
└── .env / .env.local          [Environment variables]
```

### Component Hierarchy

```
App.jsx (Root)
├── Login.jsx / Signup.jsx (Auth screens)
└── (When authenticated):
    ├── Navigation bar with tabs
    ├── QuizWizard (Tab: "Quiz")
    │   ├── ProgressBar
    │   ├── Question rendering
    │   └── Results (displays when quiz complete)
    ├── CareerList (Tab: "Browse Careers")
    │   └── CareerDetail (modal/expanded view)
    │       ├── SkillGap (skill gap analysis)
    │       └── Roadmap
    └── Profile (Tab: "Profile")
        ├── User info
        ├── Saved bookmarks
        └── Quiz history (can reopen past results)
```

### State Management

```
App.jsx (main state):
  - user: User profile from token
  - loading: Initial auth state
  - view: Current tab (quiz|careers|profile)
  - showSignup: Auth form toggle
  - careerToOpen: Which career to open in CareerList

Component-level state:
  - QuizWizard: answers dict, current question, submitted flag
  - CareerList: careers list, selected career, search filters
  - Profile: user skills, bookmarks, history
```

### Navigation Flow

```
User Path 1: Quiz → Results → Career Detail
  1. User takes quiz in QuizWizard
  2. Results shows top 5 careers
  3. User clicks career card
  4. onNavigateToCareer() callback fires
  5. App switches to "careers" tab
  6. CareerList receives careerToOpen prop
  7. useEffect auto-opens that career

User Path 2: Browse → Career Detail
  1. User clicks Browse Careers tab
  2. CareerList loads all 130+ careers
  3. User searches/filters
  4. User clicks career
  5. CareerDetail modal opens with roadmap and skill gap

User Path 3: Profile → History → Career Detail
  1. User goes to Profile tab
  2. Views past quiz results
  3. Clicks result to see top careers
  4. Clicks career from results
  5. Opens career detail
```

---

## ML Algorithm Details

### Algorithm: Cosine Similarity (Vector-Based Matching)

#### Formula
```
similarity(user, career) = (user · career) / (||user|| × ||career||)

where:
  user · career     = sum of element-wise products
  ||user||          = sqrt(sum of user² elements)
  ||career||        = sqrt(sum of career² elements)
  
Result: [0, 1]
  0 = completely different orientation
  1 = identical orientation
  0.85+ = good match (recommend)
```

#### Vector Dimensions (80-dimensional)

```
Indices 0-19: Q1-Q20 (Continuous)
  [0-4]:   Q1-Q5 (Cognitive & Problem Solving)
  [5-9]:   Q6-Q10 (Creativity & Innovation)
  [10-14]: Q11-Q15 (Communication & Leadership)
  [15-19]: Q16-Q20 (Academic & Technical)
  
Indices 20-79: Q21-Q35 (One-hot encoded, 15 questions × 4 options)
  [20-23]: Q21 (A/B/C/D = 4 dims)
  [24-27]: Q22 (A/B/C/D = 4 dims)
  [28-31]: Q23 (A/B/C/D = 4 dims)
  [32-35]: Q24 (A/B/C/D = 4 dims)
  [36-39]: Q25 (A/B/C/D = 4 dims)
  [40-43]: Q26 (A/B/C/D = 4 dims)
  [44-47]: Q27 (A/B/C/D = 4 dims)
  [48-51]: Q28 (A/B/C/D = 4 dims)
  [52-55]: Q29 (A/B/C/D = 4 dims)
  [56-59]: Q30 (A/B/C/D = 4 dims)
  [60-63]: Q31 (A/B/C/D = 4 dims)
  [64-67]: Q32 (A/B/C/D = 4 dims)
  [68-71]: Q33 (A/B/C/D = 4 dims)
  [72-75]: Q34 (A/B/C/D = 4 dims)
  [76-79]: Q35 (A/B/C/D = 4 dims)
```

#### Process Flow

```
1. User submits 35 answers
   ↓
2. Validate answers (all 35 present, correct ranges)
   ↓
3. Convert to 80-dim vector:
   - Q1-Q20: normalize to [0, 1]
   - Q21-Q35: one-hot encode
   ↓
4. Load career vectors (130+ careers from ML system)
   ↓
5. Apply feature weights:
   - Cognitive: 1.2x
   - Creativity: 1.0x
   - Communication: 1.1x
   - Academic: 1.2x
   - Preferences: 1.5x (highest)
   ↓
6. For each career:
   - Calculate cosine similarity
   - Store (career_name, score)
   ↓
7. Sort by score descending, take top 5
   ↓
8. Generate explanations for each
   ↓
9. Save to database (UserResult)
   ↓
10. Return JSON with top 5, scores, explanations
```

#### Why Vector Matching?

```
Pros:
  ✓ Fast: O(n×d) where n=130 careers, d=80 dims
  ✓ Interpretable: similarity = angle between vectors
  ✓ Normalized: 0-1 scale naturally
  ✓ No ML training: pure mathematics
  ✓ Explainable: understand which features matter

Cons (handled):
  ✗ Requires pre-designed vectors → solved by expert design
  ✗ Linear only → sufficient for this problem
```

---

## API Specification

### Base URL
```
http://localhost:8000/api/
```

### Authentication
```
Token-based (HTTP header):
  Authorization: Token <token string>
```

### Endpoints

#### Authentication

**POST /auth/signup/**
```json
Request:
{
  "email": "user@example.com",
  "username": "john_doe",
  "password": "secure_password"
}

Response (201):
{
  "success": true,
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "user@example.com"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**POST /auth/login/**
```json
Request:
{
  "email": "user@example.com",
  "password": "secure_password"
}

Response (200):
{
  "success": true,
  "message": "Login successful",
  "user": {...},
  "token": "..."
}
```

**GET /auth/profile/**
```json
Request: (Auth required)
  Authorization: Token <token>

Response (200):
{
  "profile": {
    "id": 1,
    "username": "john_doe",
    "email": "user@example.com",
    "skills": [...],
    "bookmarks": [...]
  }
}
```

#### Predictions

**POST /predict/**
```json
Request: (Auth required)
{
  "answers": {
    "q1": 8,
    "q2": 7,
    "q3": 9,
    ...
    "q20": 8,
    "q21": "A",
    "q22": "B",
    "q23": "C",
    ...
    "q35": "D"
  },
  "save_result": true
}

Response (200):
{
  "success": true,
  "predictions": {
    "top_careers": [
      {
        "rank": 1,
        "career": "Software Engineer",
        "match_percentage": 92,
        "explanation": "Strong in problem solving and technical skills",
        "description": "Design and develop software applications..."
      },
      ...
    ],
    "profile": {
      "abilities": {...},
      "work_style": {...},
      "interests": {...}
    }
  },
  "result_id": "uuid..."
}
```

**GET /predict/history/**
```json
Request: (Auth required)

Response (200):
{
  "results": [
    {
      "id": "uuid",
      "created_at": "2026-03-01T10:30:00Z",
      "top_careers": [...],
      "profile_snapshot": {...}
    },
    ...
  ]
}
```

#### Careers

**GET /careers/**
```json
Response (200):
{
  "count": 130,
  "next": "http://localhost:8000/api/careers/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "name": "Software Engineer",
      "category": "technology",
      "demand_level": "high",
      "salary_min": 80000,
      "salary_max": 150000
    },
    ...
  ]
}
```

**GET /careers/{id}/**
```json
Response (200):
{
  "id": "uuid",
  "name": "Software Engineer",
  "description": "Design and develop...",
  "category": "technology",
  "demand_level": "high",
  "salary_min": 80000,
  "salary_max": 150000,
  "required_skills": [
    {
      "skill": "Python",
      "proficiency": "intermediate",
      "category": "technical"
    },
    ...
  ]
}
```

**GET /careers/{id}/roadmap/**
```json
Response (200):
{
  "roadmap": [
    {
      "stage": "Entry Level",
      "duration_months": 6,
      "description": "Learn basics...",
      "skills_to_learn": ["Python", "SQL", ...]
    },
    {
      "stage": "Mid-Level",
      "duration_months": 24,
      "description": "...",
      "skills_to_learn": [...]
    },
    {
      "stage": "Senior",
      "duration_months": 36,
      "description": "...",
      "skills_to_learn": [...]
    }
  ]
}
```

**POST /careers/{id}/bookmark/**
```json
Request: (Auth required)
{
  "action": "add" | "remove"
}

Response (200):
{
  "success": true,
  "message": "Bookmarked",
  "bookmarked": true
}
```

#### Analysis

**GET /skill-gap/?career=Software Engineer**
```json
Response (200):
{
  "career": "Software Engineer",
  "user_skills": [
    {"skill": "Python", "proficiency": "intermediate"},
    ...
  ],
  "required_skills": [
    {"skill": "Python", "proficiency": "intermediate"},
    {"skill": "Java", "proficiency": "beginner"},
    ...
  ],
  "gaps": [
    {"skill": "Java", "proficiency": "beginner", "user_has": false},
    ...
  ],
  "match_percentage": 65
}
```

**GET /learning-path/?career=Software Engineer**
```json
Response (200):
{
  "career": "Software Engineer",
  "learning_path": [
    {
      "stage": 1,
      "duration": 6,
      "skills": ["Python", "SQL", "Git"],
      "resources": ["Codecademy", "FreeCodeCamp", ...]
    },
    ...
  ]
}
```

#### System

**GET /health/**
```json
Response (200):
{
  "status": "healthy"
}
```

**GET /info/**
```json
Response (200):
{
  "api_version": "1.0",
  "careers_count": 130,
  "questions_count": 35,
  "endpoints": [...]
}
```

---

## Data Flow

### Flow 1: User Takes Quiz → Gets Recommendations

```
┌──────────────────────────────────────────────┐
│ FRONTEND (React)                             │
│ User fills 35-question quiz                  │
│ Clicks Submit                                │
└────────────────────┬─────────────────────────┘
                     │ POST /predict/
                     │ {answers, save_result: true}
                     ↓
┌──────────────────────────────────────────────┐
│ BACKEND (Django)                             │
│ views.predict()                              │
│ ├─ Validate 35 answers                      │
│ ├─ Call PredictionService.predict_and_save()│
│ │  ├─ UserVectorizer.vectorize(answers)     │
│ │  ├─ CareerRecommender.recommend()         │
│ │  │  ├─ Load ML vectors                    │
│ │  │  ├─ Apply weights                      │
│ │  │  ├─ Calculate similarities (130 careers)│
│ │  │  └─ Get top 5 + explanations           │
│ │  └─ Save UserResult to database           │
│ └─ Return JSON response                     │
└────────────────────┬─────────────────────────┘
                     │ HTTP 200
                     │ {top_careers, profile}
                     ↓
┌──────────────────────────────────────────────┐
│ FRONTEND (React)                             │
│ <Results> shows top 5 with:                 │
│ ├─ Career cards with match %                │
│ ├─ Explanations                             │
│ └─ Profile charts (abilities, interests)    │
└──────────────────────────────────────────────┘
```

### Flow 2: User Clicks Career → Navigates to Browse Tab

```
┌──────────────────────────────────────────────┐
│ Results.jsx                                  │
│ User clicks career card                      │
│ onCareerClick(careerName)                    │
└────────────────────┬─────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────┐
│ App.jsx (parent)                             │
│ handleNavigateToCareer(careerName) called    │
│ ├─ setCareerToOpen(careerName)              │
│ └─ setView("careers")                       │
└────────────────────┬─────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────┐
│ CareerList.jsx                               │
│ Receives props:                              │
│ ├─ careerToOpen="Software Engineer"          │
│ useEffect fires:                             │
│ ├─ Find career in list                      │
│ └─ openCareer(careerItem)                    │
└────────────────────┬─────────────────────────┘
                     │ GET /careers/{id}/
                     ↓
┌──────────────────────────────────────────────┐
│ BACKEND returns career details               │
│ + roadmap + required skills                 │
└────────────────────┬─────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────┐
│ CareerDetail.jsx (modal)                    │
│ Display:                                    │
│ ├─ Career name + description                │
│ ├─ Roadmap (3 stages)                       │
│ ├─ Required skills                          │
│ ├─ Skill gap analysis                       │
│ └─ Bookmark button                          │
└──────────────────────────────────────────────┘
```

### Flow 3: User Views Profile History

```
┌──────────────────────────────────────────────┐
│ Profile.jsx                                  │
│ User logged in                               │
│ GET /auth/profile/                           │
│ ├─ Load user info                           │
│ ├─ Load bookmarks                           │
│ └─ GET /predict/history/                    │
│    Load past quiz results                   │
└────────────────────┬─────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────┐
│ Display:                                    │
│ ├─ User name, email, skills                 │
│ ├─ Bookmarked careers                       │
│ └─ Results history:                         │
│    - Quiz result 1 (Mar 3)                  │
│    - Quiz result 2 (Mar 1)                  │
│    (Click to reopen top careers)            │
└──────────────────────────────────────────────┘
```

---

## Authentication & Authorization

### Token-Based Authentication

#### How It Works
```
1. User signup/login
   ↓ POST /auth/signup/ or /auth/login/
   ↓ Backend creates User + Token
   ↓ Returns {user, token}
   
2. Frontend stores token in localStorage
   localStorage.setItem("token", token)
   
3. Subsequent requests include token
   Authorization: Token <token>
   
4. Backend validates token before returning data
   @permission_classes([IsAuthenticated])
```

#### Protected Endpoints
```
Requires token:
  - GET /auth/profile/
  - POST /predict/
  - GET /predict/history/
  - POST /careers/{id}/bookmark/
  - GET /skill-gap/
  - GET /learning-path/

Public endpoints (no token):
  - POST /auth/signup/
  - POST /auth/login/
  - GET /careers/
  - GET /careers/{id}/
  - GET /careers/{id}/roadmap/
  - GET /health/
  - GET /info/
```

#### Session Management
```
Frontend:
  - Store token & user in state
  - Check localStorage on app load
  - Clear on logout

Backend:
  - Token stored in database
  - Validated on every request
  - Can be revoked (future feature)
```

---

## Performance & Scalability

### Metrics

#### Time Complexity
```
Operation                Complexity    Time
─────────────────────────────────────────
Answer validation        O(35)         <1ms
Vector creation          O(35+80)      <1ms
Load career vectors      O(1)          <1ms
Apply weights            O(40)         <1ms
Similarity calculation   O(130×40)     ~10ms
Get top 5               O(130 log 5)   ~2ms
Generate explanations    O(5)          ~2ms
Database save            O(1)          ~5-10ms
──────────────────────────────────────────
Total                                  ~30ms
```

#### Space Complexity
```
User vector           80 × 8 bytes    640 bytes
Career vectors (130)  130 × 80 × 8    83.2 KB
Weights              80 × 8 bytes     640 bytes
Results              130 × 8 bytes    1.04 KB
────────────────────────────────────────────
Per-request memory                    ~85 KB
```

### Scalability Analysis

#### Current (130 careers)
- Time per recommendation: ~40ms
- Throughput: ~25 req/sec per server
- Memory: ~85 KB per request (minimal)
- DB queries: ~2 (validate user, save result)

#### Scaled to 1000 careers
- Time: O(1000 × 80) = ~200ms
- Throughput: ~5 req/sec
- Still acceptable for web

#### Optimizations Available
```
If needed:
  ✓ Cache career vectors in memory
  ✓ Use async task queue (Celery) for save
  ✓ Implement result pagination
  ✓ Add Redis caching for popular careers
  ✓ Use approximate nearest neighbors (ANN)
```

### Deployment Architecture

#### Development
```
Frontend:  npm start (port 3000)
Backend:   python manage.py runserver (port 8000)
Database:  SQLite (db.sqlite3)
Static:    Served by Django dev server
```

#### Production
```
Frontend:
  ├─ Build: npm run build
  └─ Serve via: Nginx + CloudFront CDN

Backend:
  ├─ App: Gunicorn (8-16 workers)
  ├─ Proxy: Nginx (load balancer)
  ├─ Database: PostgreSQL (upgrade from SQLite)
  └─ Cache: Redis (optional, for result caching)

Static Files:
  ├─ Admin CSS/JS collected
  └─ Served from /staticfiles/
```

---

## Summary of Changes from Original Design

### What's New in Current Implementation

1. **Database Integration**
   - Originally: Stateless (all ML in memory)
   - Now: 9 Django models store user data, careers, results, skills

2. **Authentication**
   - Originally: None
   - Now: Token-based auth with signup/login

3. **Result Persistence**
   - Originally: Results only returned in response
   - Now: Results saved to database, accessible in history

4. **Expanded Career Set**
   - Originally: 90 careers
   - Now: 130+ careers with auto-categorization

5. **User Features**
   - Originally: Just recommendations
   - Now: Bookmarks, skill tracking, result history, profile

6. **Frontend Architecture**
   - Originally: Simple quiz → results view
   - Now: Tab-based (Quiz, Browse, Profile) with modal detail views

7. **Analysis Features**
   - Originally: Just similarity scores
   - Now: Skill gap analysis, learning paths, roadmaps

8. **Data Persistence**
   - Originally: In-memory only
   - Now: SQLite with 9 models, migrations, ORM

---

## Key Files to Understand

### Backend
- `settings.py` - Django config (INSTALLED_APPS, DATABASES, STATIC_FILES)
- `career_app/models.py` - All 9 data models
- `career_app/views.py` - 18 API endpoints
- `career_app/services.py` - Business logic (PredictionService, SkillGapService)
- `ml/recommender.py` - Core recommendation algorithm
- `ml/careers.py` - 130 career vectors and metadata

### Frontend
- `App.jsx` - Root component, tab navigation, state management
- `api.js` - API service wrapper for all endpoints
- Individual components: Login, Signup, QuizWizard, Results, CareerList, Profile
- `index.css` - Global styles

This architecture is **production-ready**, **horizontally scalable**, and **easily extensible** to add more careers, questions, or features.
