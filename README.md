# Lead Scoring Backend

## Overview
Backend service to upload leads, define product offers, and score each lead's buying intent (High/Medium/Low) using rule-based + AI logic.

## Features
- Create offers via `/offer/` (POST)
- Upload leads via CSV `/leads/upload/` (POST)
- Score leads combining Rule Layer + AI Layer `/score/` (POST)
- View results `/results/` (GET)
- Export results as CSV `/results/export/` (GET)
- Unit tests for rule-based scoring

## Setup

1. Clone repo:
git clone <REPO_URL>
cd leadScoring


## Create virtual environment:
python -m venv env
env\Scripts\activate  # Windows
source env/bin/activate  # Linux/Mac


## Install dependencies:
pip install -r requirements.txt


## Run migrations:
python manage.py migrate

## Run server locally:
python manage.py runserver

## API Endpoints
POST /offer/
Request JSON:

    {
        "name": "AI Outreach Automation",
        "value_props": ["24/7 outreach", "6x more meetings"],
        "ideal_use_cases": ["B2B SaaS mid-market"]
    }

## Upload Leads
    POST /leads/upload/
    CSV file with columns:
        
        name,role,company,industry,location,linkedin_bio


## 4. Get Results
    GET /results/
    Returns all lead scores in JSON.
## 5. Export CSV

    GET /results/export/
    Download scored leads as CSV.
## Scoring Logic

    Rule Layer (max 50 points)

    Role relevance: decision maker (+20), influencer (+10)

    Industry match: exact ICP (+20), adjacent (+10)

    Data completeness: all fields present (+10)

    AI Layer (max 50 points)

    High intent → +50

    Medium intent → +30

    Low intent → +10

    Reasoning added to reasoning field

    Final Score = rule_score + ai_points
    Intent = High / Medium / Low


## Testing
python manage.py test

## Deployment 
Currently runs locally at `http://127.0.0.1:8000/`
    - To deploy publicly, use platforms like Render, Railway, or Heroku
    - Make sure to update `ALLOWED_HOSTS` in `settings.py`
    - Include `requirements.txt` and `Procfile` for deployment


##  AI Integration
AI Layer classifies lead intent as High / Medium / Low
    - Currently uses a stub function returning Medium intent
    - In production, can integrate OpenAI, Gemini, or any AI provider
    - AI output adds points (High=50, Medium=30, Low=10) and reasoning to final score




