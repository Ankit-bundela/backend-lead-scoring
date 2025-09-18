# Lead Scoring Backend

## Overview
Backend service to upload leads, define product offers, and score each lead's buying intent (High/Medium/Low) using rule-based + AI logic.

This service allows sales/marketing teams to quickly qualify leads using both deterministic rules and AI reasoning.

## Features
- Create offers via `/offer/` (POST)
- Upload leads via CSV `/leads/upload/` (POST)
- Score leads combining Rule Layer + AI Layer `/score/` (POST)
- View results `/results/` (GET)
- Export results as CSV `/results/export/` (GET)
- Unit tests for rule-based scoring

## Setup

### 1. Clone repo
```bash
git clone https://github.com/Ankit-bundela/backend-lead-scoring.git
cd backend-lead-scoring
```
## Create virtual environment
    python -m venv env
# Windows
    env\Scripts\activate
# Linux/Mac
    source env/bin/activate

### 3. Install dependencies
    pip install -r requirements.txt

### 4. Run migrations
    python manage.py migrate

## 5. Run server locally
    python manage.py runserver


# API Endpoints
### 1. Create Offer
    POST /offer/
    Request JSON:
    {
        "name": "AI Outreach Automation",
        "value_props": ["24/7 outreach", "6x more meetings"],
        "ideal_use_cases": ["B2B SaaS mid-market"]
    }
### 2. Upload Leads

    POST /leads/upload/
    Upload CSV file with columns:
    name,role,company,industry,location,linkedin_bio

### 3. Score Leads

    POST /score/
    Request JSON:
    {
        "offer_id": 1
    }
### 4. Get Results

    GET /results/

# Scoring Logic

## Rule Layer (max 50 points)

    Role relevance: decision maker (+20), influencer (+10)

    Industry match: exact ICP (+20), adjacent (+10)

    Data completeness: all fields present (+10)

## AI Layer (max 50 points)

    High intent → +50 points

    Medium intent → +30 points

    Low intent → +10 points

    Reasoning added to reasoning field

## Final Score

Final Score = rule_score + ai_points
Intent = High / Medium / Low

## Testing

python manage.py test

# Deployment

    Currently runs locally at http://127.0.0.1:8000/

    To deploy publicly, use platforms like Render, Railway, or Heroku

    Update ALLOWED_HOSTS in settings.py before deployment

    Include requirements.txt and Procfile for deployment

    Example live URL: https://backend-lead-scoring-1yxh.onrender.com

# AI Integration

    AI Layer classifies lead intent as High / Medium / Low

    Currently uses a stub function returning Medium intent

    In production, integrate OpenAI, Gemini, or any AI provider

    AI output adds points (High=50, Medium=30, Low=10) and reasoning to final score
