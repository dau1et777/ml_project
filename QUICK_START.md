# 🚀 QUICK START GUIDE

## One-Command Setup (Windows)

### Step 1: Terminal 1 - Backend
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 2: Terminal 2 - Frontend
```powershell
cd frontend
npm install
npm start
```

Expected output:
```
Compiled successfully!
You can now view career-recommendation-frontend in the browser.
  Local:            http://localhost:3000
```

### Step 3: Open Browser
- Visit http://localhost:3000
- Take the quiz
- Get recommendations!

---

## Testing Without Frontend

### Test in Python Terminal

From `ml/` directory:

```python
import sys
sys.path.insert(0, 'backend')

from ml.recommender import recommend_careers

answers = {
    "q1": 9, "q2": 8, "q3": 9, "q4": 8, "q5": 8,
    "q6": 5, "q7": 4, "q8": 6, "q9": 7, "q10": 5,
    "q11": 3, "q12": 2, "q13": 3, "q14": 3, "q15": 2,
    "q16": 9, "q17": 7, "q18": 9, "q19": 9, "q20": 8,
    "q21": "A", "q22": "A", "q23": "C", "q24": "A", "q25": "A"
}

results = recommend_careers(answers, debug=True)

for rec in results["recommendations"]:
    print(f"{rec['rank']}. {rec['career']} ({rec['match_percentage']}%)")
    print(f"   {rec['explanation']}\n")
```

### Run Test Script

```powershell
cd ml
python test_ml_system.py
```

This will:
✓ Validate quiz logic
✓ Test vectorization
✓ Check all 90 career vectors
✓ Verify weighting system
✓ Test cosine similarity
✓ Run full recommendation
✓ Test different profiles

---

## Testing API Endpoint (cURL)

```bash
curl -X POST http://localhost:8000/api/recommend/ \
  -H "Content-Type: application/json" \
  -d '{
    "answers": {
      "q1": 9, "q2": 8, "q3": 9, "q4": 8, "q5": 8,
      "q6": 5, "q7": 4, "q8": 6, "q9": 7, "q10": 5,
      "q11": 3, "q12": 2, "q13": 3, "q14": 3, "q15": 2,
      "q16": 9, "q17": 7, "q18": 9, "q19": 9, "q20": 8,
      "q21": "A", "q22": "A", "q23": "C", "q24": "A", "q25": "A"
    }
  }'
```

---

## Common Issues

### Port Already in Use

Port 8000 taken:
```bash
python manage.py runserver 8001
```

Port 3000 taken:
```bash
PORT=3001 npm start
```

### Module Not Found

Make sure you're in correct directory:
```bash
# Backend
cd ml/backend

# Frontend  
cd ml/frontend
```

### CORS Error

Check Django settings CORS_ALLOWED_ORIGINS includes http://localhost:3000

### Slow First Load

First quiz load compiles 90 career vectors - normal, takes ~1 second

---

## Debug Mode

### Enable API Debug
```json
{
  "answers": {...},
  "debug": true
}
```

Returns user vector, weighted vector, and top 5 career vectors.

### Print Explanation
```python
from ml.debug import debug_recommendation

results = recommend_careers(answers)
debug_recommendation(answers, results)
```

---

## File Structure for Reference

```
ml/
├── backend/
│   ├── ml/
│   │   ├── validator.py       ← Quiz validation
│   │   ├── vectorizer.py      ← Answers → 40-dim vector
│   │   ├── careers.py         ← 90 career vectors
│   │   ├── weights.py         ← Feature weights
│   │   ├── similarity.py      ← Cosine similarity
│   │   ├── recommender.py     ← Main logic
│   │   └── debug.py           ← Debugging
│   ├── views.py               ← REST endpoints
│   ├── urls.py                ← URL routing
│   ├── settings.py            ← Django config
│   ├── manage.py              ← Django CLI
│   └── requirements.txt        ← Dependencies
│
├── frontend/
│   ├── src/
│   │   ├── QuizWizard.jsx     ← Main quiz
│   │   ├── ProgressBar.jsx    ← Progress tracking
│   │   ├── Results.jsx        ← Results display
│   │   ├── api.js             ← API calls
│   │   └── ...styles
│   ├── public/
│   │   └── index.html         ← HTML entry
│   ├── package.json           ← Dependencies
│   └── .env                   ← Config
│
├── test_ml_system.py          ← Full test suite
├── README.md                  ← Full documentation
└── QUICK_START.md            ← This file
```

---

## Success Indicators

✅ Backend starts without errors
✅ Frontend compiles successfully
✅ Quiz loads in browser
✅ Can answer questions  
✅ Submit returns results
✅ Top 5 careers show with percentages
✅ Explanations are provided
✅ Profile charts appear at top of results

---

## Next Steps

1. **Customize** - Modify careers.py for your domain
2. **Deploy** - Set DEBUG=False in settings.py
3. **Scale** - Add more careers (currently 90)
4. **Enhance** - Add user persistence, history tracking

---

Good luck! 🚀
