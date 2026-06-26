# Job Market Signal Tracker

A live automated data pipeline that tracks real-time job market trends, skill demand, and salary insights across 700+ job postings — covering data, tech, marketing, design, sales and more.

🔴 Live Dashboard: https://job-market-tracker-a5xvb7wwilsoyxhcqvtyyf.streamlit.app/

📁 GitHub: https://github.com/fizzaassad/job-market-tracker

---

## The Problem

Job seekers and students waste time learning skills that are declining in demand. This tool provides data-driven answers to:
- Which skills are most in demand right now?
- Which skills are you missing for your target role?
- What salary should you expect?
- How is skill demand changing over time?

---

## What I Built

A fully automated production-grade data pipeline that:
1. Collects 300+ job postings daily from 2 APIs (RemoteOK, The Muse)
2. Extracts 25+ in-demand skills using NLP and regex patterns
3. Stores everything in a Supabase cloud PostgreSQL database with no duplicates
4. Runs automatically every day via GitHub Actions — no laptop needed
5. Keeps Supabase database alive with daily ping to prevent pausing
6. Visualizes trends on a live interactive dashboard
7. Includes a Skills Gap Analyzer — enter any job title and see exactly which skills you are missing
8. Works for ALL job types — Data, Tech, Marketing, Design, Sales, and more

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
| REST APIs | Live data collection from RemoteOK and The Muse |
| GitHub Actions | Automated daily pipeline — runs without laptop |
| Git and GitHub | Version control |

---

## Key Findings (Based on 704 Real Job Postings)

- Communication is the most in-demand skill overall, appearing in 38.9% of all postings
- 78.3% of all positions are fully remote across all industries
- 513 unique companies are actively hiring across both platforms
- Excel and Power BI appear in 100% of Data Analyst job postings — Python alone is not enough
- SQL remains essential across all data roles regardless of seniority
- Project Management and Leadership are top skills for non-technical roles
- Real trend data collected and tracked daily since June 2026

---

## Features

- Key metrics dashboard — top skill, remote percentage, companies hiring
- Skill demand bar chart — top 15 skills employers actually want
- Trends over time — 3 weeks of real historical data showing skill demand changes
- Salary distribution — understand what to expect per role
- Skills Gap Analyzer — works for ANY role including Data, Marketing, Design, and Sales
- Job search table — browse and filter 700+ real job postings
- About section with real project findings and story

---

## How the Automation Works

Every day automatically with no laptop needed:
- GitHub Actions server wakes up at 10pm Pakistan time
- Pings Supabase to keep database alive and prevent pausing
- Fetches 200+ fresh jobs from 2 APIs
- Saves new jobs to Supabase and skips duplicates
- Dashboard updates automatically for all visitors

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

├── .github/

│   └── workflows/

│ 
└── scraper.yml       — GitHub Actions daily automation

├── src/

│   ├── scrapper.py           — Collects job data from 2 APIs

│   ├── processor.py          — Cleans and extracts skills
│   └── database.py           — Supabase cloud database operations
├── dashboard/
│   └── app.py                — Streamlit interactive dashboard
├── data/                     — Local JSON backup files
├── .env                      — Credentials not on GitHub
├── .gitignore
└── requirements.txt

---

## Skills Tracked 25+

Data and Tech: Python, SQL, Excel, Tableau, Power BI, Machine Learning, AWS, Docker, Git, JavaScript, React, PostgreSQL

Marketing: SEO, Social Media, Content Writing, Google Ads, Email Marketing

Design: Figma, Adobe Photoshop, UI/UX Design

Sales and Business: Salesforce, Negotiation, CRM

Soft Skills: Communication, Leadership, Project Management, Customer Service

---

## About

Built by Fiza Asad as a self-directed data engineering and analysis project to solve a real personal problem — figuring out which skills the job market actually demands, based on data rather than opinions.

When I started learning Data Science I had one problem — I did not know which skills to learn first. Everyone gives different advice. So I built this tool to answer that question with real data instead of opinions.
Connect: https://www.linkedin.com/in/fiza-asad-9b9a88288/




Currently applying for Masters programs in AI and Data Science in Germany, South Korea, Japan, and China.

Connect: https://www.linkedin.com/in/fiza-asad-9b9a88288/
