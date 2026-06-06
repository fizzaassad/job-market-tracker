# Job Market Signal Tracker

A live data pipeline that tracks real-time job market trends, 
skill demand, and salary insights across 300+ daily job postings.

🔴 Live Dashboard: https://job-market-tracker-a5xvb7wwilsoyxhcqvtyyf.streamlit.app/

---

## The Problem
Job seekers and students waste time learning skills that are 
declining in demand. This tool provides data-driven answers to:
- Which skills are most in demand right now?
- Which cities are hiring the most?
- What salary should you expect for each skill?

---

## What I Built
A fully automated data pipeline that:
1. Collects 300+ job postings daily from 2 APIs (RemoteOK, The Muse)
2. Extracts 12 in-demand skills using NLP and regex patterns
3. Stores everything in a SQLite database (no duplicates)
4. Visualizes trends on a live interactive dashboard

---

## Tech Stack
| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| Pandas | Data cleaning and analysis |
| SQLite | Database storage |
| Regex/NLP | Skill extraction from job descriptions |
| Plotly | Interactive charts |
| Streamlit | Dashboard deployment |
| REST APIs | Live data collection |
| Git/GitHub | Version control |

---

## Key Findings
- **Python** is the most in-demand skill appearing in 65%+ of postings
- **SQL** remains essential across all data roles
- **Remote jobs** grew significantly in tech and data roles
- **Machine Learning** skills command higher salaries than average

---

## How To Run Locally
1. Clone the repository
   git clone https://github.com/fizzaassad/job-market-tracker.git

2. Install dependencies
   pip install -r requirements.txt

3. Collect data
   cd src
   python scraper.py

4. Launch dashboard
   cd dashboard
   streamlit run app.py

---

## Project Structure
job_market_tracker/
├── src/
│   ├── scraper.py       # Collects job data from APIs
│   ├── processor.py     # Cleans and extracts skills
│   └── database.py      # SQLite database operations
├── dashboard/
│   └── app.py           # Streamlit dashboard
├── data/                # Local database and JSON files
└── requirements.txt

---

## About
Built by Fiza Asad as part of a self-directed data engineering 
and analysis project. Currently pursuing opportunities in 
Data Science and AI.

Connect: https://www.linkedin.com/in/fiza-asad-9b9a88288/
