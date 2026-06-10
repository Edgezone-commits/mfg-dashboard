# Manufacturing Operations Dashboard

A browser-based morning briefing tool for manufacturing teams.
Live job status, rush order tracking, department performance,
and an AI-generated ops summary — all on one screen.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-red)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.0-orange)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## The Problem

Every morning, an operations manager has to answer the same questions
before the day starts:

- What jobs are running late?
- Which orders are flagged as urgent?
- How is each department tracking?
- What should the team focus on today?

In most manufacturing companies the answers are scattered across an ERP system,
a whiteboard, and someone's memory. Getting the full picture takes 20-30 minutes
of manual checking. This dashboard puts it on one screen, with an AI button
that writes the briefing for you.

---

## Features

| Feature | Description |
|---|---|
| KPI Strip | Total jobs, completed, rush orders, overdue, avg build time — color coded |
| AI Briefing | One click generates a plain-English morning summary from live data |
| Rush Orders | Live table of urgent jobs sorted by due date |
| Overdue Jobs | Every job past its due date and not yet complete |
| Department Stats | Job counts and avg build hours by team |
| Job Register | Full filterable table of all job orders |

---

## Architecture
data/generate_data.py  →  data/operations.db  (SQLite)
↓
src/database.py       (SQL queries)
↓
src/analytics.py      (Pandas KPIs)
↓
src/ai_summary.py     (Gemini API)
↓
app.py            (Streamlit UI)

Each layer has one responsibility. Swapping the SQLite database for a live
connection to JobBoss or AccountMate requires changing only `database.py`.
Everything else stays the same.

---

## Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/Edgezone-commits/mfg-dashboard.git
cd mfg-dashboard
```

**2. Set up environment**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install pandas streamlit google-genai python-dotenv
```

**3. Add your API key**

Create a `.env` file in the root:
GEMINI_API_KEY=your-key-here
Get a free key at [aistudio.google.com](https://aistudio.google.com)

**4. Generate the database**
```bash
python data/generate_data.py
```

**5. Run**
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

---

## Project Structure
mfg-dashboard/
├── app.py                  # Streamlit UI
├── data/
│   ├── generate_data.py    # Creates SQLite database with sample jobs
│   └── operations.db       # Auto-generated (not in git)
├── src/
│   ├── database.py         # SQL queries
│   ├── analytics.py        # Pandas KPI calculations
│   └── ai_summary.py       # Gemini API call
├── .env                    # API key (not in git)
├── .gitignore
└── requirements.txt

---

## Stack

- **Python 3.13**
- **Streamlit** — web interface
- **SQLite** — local database simulating ERP data
- **Pandas** — data manipulation and KPI calculation
- **Google Gemini 2.0 Flash** — AI briefing generation
- **python-dotenv** — environment variable management

---

## About the Data

The database contains 50 synthetic job orders with realistic manufacturing fields:
customer names, products, departments, due dates, estimated vs actual build times,
rush flags, and completion status.

This simulates what would live in a shop floor ERP like JobBoss.
In a real deployment, `src/database.py` would connect to the actual system via ODBC.

---

## What I Would Add Next

- Direct ODBC connection to AccountMate or JobBoss
- Auto-email the morning briefing at 7am via scheduled task
- On-time delivery rate trend chart for the last 30 days
- Manager notes on individual jobs from within the dashboard
- SMS alert when a rush order goes overdue

---

## Why I Built This

This came out of researching the AI & Automation Intern role at Mifab.
The job description mentioned inventory optimization, operational reporting,
and an AI-powered assistant — I wanted to build something that touched all
three areas in a realistic manufacturing context.

The hardest part was not the code. It was understanding what an operations
manager actually needs to see at 7am, and designing around that instead of
around what was easy to build.
