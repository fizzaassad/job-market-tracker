# Job Market Signal Tracker

A live data pipeline that tracks real-time job market trends, skill demand, and salary insights across 300+ daily job postings.

🔴 Live Dashboard: https://job-market-tracker-a5xvb7wwilsoyxhcqvtyyf.streamlit.app/

---

## The Problem
Job seekers and students waste time learning skills that are declining in demand. This tool provides data-driven answers to:
- Which skills are most in demand right now?
- Which cities are hiring the most?
- What salary should you expect for each skill?
- Which skills are you missing for your target role?

---

## What I Built
A fully automated data pipeline that:
1. Collects 300+ job postings daily from 2 APIs (RemoteOK, The Muse)
2. Extracts 12 in-demand skills using NLP and regex patterns
3. Stores everything in a Supabase cloud database with no duplicates
4. Visualizes trends on a live interactive dashboard
5. Includes a Skills Gap Analyzer — enter any job title and see exactly which skills you are missing

---

## Tech Stack
| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| Pandas | Data cleaning and analysis |
| Supabase PostgreSQL | Cloud database storage |
| Regex and NLP | Skill extraction from job descriptions |
| Plotly | Interactive charts |
| Streamlit | Dashboard deployment |
| REST APIs | Live data collection |
| Git and GitHub | Version control |

---

## Key Findings
- Python is the most in-demand skill appearing in 65% of all postings
- Excel and Power BI appear in 100% of Data Analyst job postings — Python alone is not enough
- SQL remains essential across all data roles
- Remote positions make up the majority of tech job postings
- Machine Learning skills are growing in demand week over week

---

## Features
- Skill demand bar chart — see what employers actually want
- Trends over time — track which skills are rising or falling
- Salary distribution — understand what to expect
- Skills Gap Analyzer — find exactly what you need to learn
- Job search table — browse and filter all collected jobs

---

## How To Run Locally

Step 1 — Clone the repository
git clone https://github.com/fizzaassad/job-market-tracker.git

Step 2 — Install dependencies
pip install -r requirements.txt

Step 3 — Create a .env file in the root folder
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

Step 4 — Collect data
cd src
python scrapper.py

Step 5 — Launch dashboard
cd dashboard
streamlit run app.py

---

## Project Structure

job_market_tracker/
├── src/
│   ├── scrapper.py      — Collects job data from 2 APIs
│   ├── processor.py     — Cleans and extracts skills
│   └── database.py      — Supabase database operations
├── dashboard/
│   └── app.py           — Streamlit dashboard
├── data/                — Local JSON backup files
├── .env                 — Credentials not on GitHub
└── requirements.txt

---

## About
Built by Fiza Asad as a self-directed data engineering and analysis project. Currently pursuing opportunities in Data Science and AI and applying for Masters programs in AI and Data Science.

Connect: https://www.linkedin.com/in/fiza-asad-9b9a88288/