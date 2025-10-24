# AetherSense — Architecture & Execution Plan
_Last updated: Oct 23, 2025_

---

## 1. Problem & Vision

**Problem:**  
Travelers and photographers waste time visiting scenic spots when visibility is poor (fog, haze, low clouds, murky water).

**Vision:**  
AetherSense is a web app that predicts the best time for clear views and optimal photography at any location.

**One-line value:**  
> “For Neuschwanstein this weekend, go Sat 14:00–16:00 (94/100 visibility) — clear skies, low haze, perfect light.”

---

## 2. Scope

**In (MVP):**
- Web UI for querying visibility by location and date (Europe only).
- Visibility Score (0–100) + short human-readable explanation.
- 3–5 demo locations with deterministic results for presentation.

**Out (for now):**
- Global coverage, personalization, crowd prediction, or mobile app.

---

## 3. Key User Stories

| User Story | Acceptance Criteria |
|-------------|---------------------|
| **Query Visibility** – User asks “Best time tomorrow at Plitvice?” | Returns top 2–3 time windows with reasons in <3s |
| **Explain Factors** – User sees cloud %, haze index, sunlight angle | Shows 3+ contributing factors |
| **Demo Stability** – Judges test 3 locations | Demo locations always respond <2s |

---

## 4. System Overview

**Components**
- **Frontend:** React app (query form, results view, map).
- **Backend:** FastAPI (endpoints, data access, scoring).
- **Database:** PostgreSQL (locations, scores, logs).
- **Scoring Service:** Combines cloud, haze, and light metrics → score 0–100.
- **Cache:** Optional Redis for fast responses.
- **Deployment:** Render (backend), Vercel (frontend).

> Note: Only architecture and pseudocode are prepared before the hackathon. Implementation code begins during hack weekend.

---

## 5. Data Sources

- **Copernicus Data Space APIs**  
  - Sentinel-2 → cloud cover, water clarity.  
  - Sentinel-5P → aerosol index (haze).  
- **Solar position** calculated locally per location/time window.

---

## 6. Database Schema (Design Only)


---

## 7. API Design (Specification Only)

## 8. Scoring Algorithm (Pseudocode)
## 7. API Design (Specification Only)
## 7. API Design (Specification Only)
## 7. API Design (Specification Only)


