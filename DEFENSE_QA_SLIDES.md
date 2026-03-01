# Defense Q&A — Single-Slide Bullet Points

## Q1: How accurate is it?

- **Goal:** 85–95% logical alignment with expert judgment (not statistical prediction)
- **Validation:** Unit tests on all modules + hand-crafted user profiles
- **Top matches:** Reflect expert expectations in test scenarios
- **Deterministic:** Same answers → same results (reproducible)
- **Improvement path:** Better career vectors + real user feedback → higher accuracy
- **Proof:** Run `test_ml_system.py` during defense to show all tests pass

---

## Q2: Why cosine similarity?

- **What it measures:** How two profiles point in the same *direction* (pattern match, not magnitude)
- **Analogy:** Two arrows in space; similarity = how much they point the same way
- **Why it works:** Users with same pattern but different scales get similar recommendations
- **Speed:** Fast, simple, deterministic
- **Demo:** u=[1,2,3], c=[2,1,3] → dot product=13, |u|=√14, |c|=√14 → cosine=13/14≈**92.9%**

---

## Q3: How do weights affect results?

- **Purpose:** Tell system which trait groups matter more
- **Examples:**
  - Preferences: 1.5× (user's explicit choices count most)
  - Cognitive & Academic: 1.2× (problem-solving matters)
  - Creativity: 1.0× (baseline)
  - Communication: 1.1× (slightly important)
- **Mechanism:** Weights multiply vector values → increase contribution to dot product → shift rankings
- **Why:** They encode domain knowledge about career requirements

---

## Q4: Can it be trusted? Limitations?

- **Trust (Yes):** Fully explainable, transparent pipeline, every number visible in debug mode
- **Tested:** All modules have unit tests (show test output)
- **Limitations:**
  - Career vectors are expert-defined (may reflect bias)
  - No learning from user outcomes yet (doesn't improve over time)
- **Next steps to increase trust:**
  - Collect anonymized user feedback (did the recommendation help?)
  - Tune weights or vectors based on feedback
  - Add light, explainable learning (e.g., Bayesian updates)
- **Privacy:** Stateless design means no user data stored by default

---

## Quick Stage Tips

- **Pause after each bullet** so examiners can ask follow-ups
- **Offer to show code** if they ask: `recommender.py` orchestrates the pipeline
- **Point to tests:** Show the test suite output as proof of module correctness
- **Draw the flow** on whiteboard: Quiz → Vector → Weights → Similarity → Top 5

