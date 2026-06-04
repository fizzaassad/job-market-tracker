import streamlit as st
import pandas as pd
import plotly.express as px
import json

import re
from collections import Counter
import sqlite3
import requests
import json
from collections import Counter

@st.cache_data(ttl=3600)  # cache for 1 hour
def fetch_jobs():
    jobs = []
    
    # RemoteOK
    try:
        r = requests.get("https://remoteok.com/api", 
                        headers={"User-Agent": "JobMarketTracker/1.0"})
        jobs.extend(r.json()[1:])
    except:
        pass
    
    # The Muse
    try:
        for page in range(1, 4):
            r = requests.get("https://www.themuse.com/api/public/jobs",
                           params={"page": page, "per_page": 100})
            data = r.json()
            for job in data.get("results", []):
                jobs.append({
                    "position": job.get("name", ""),
                    "company":  job.get("company", {}).get("name", ""),
                    "description": job.get("contents", ""),
                })
    except:
        pass
    
    return jobs

jobs = fetch_jobs()
df = pd.DataFrame(jobs)
st.success(f"Loaded {len(df)} live jobs")

# ── Skill extraction ───────────────────────────
SKILLS = {
    "Python": r"\bpython\b",
    "SQL": r"\bsql\b",
    "Excel": r"\bexcel\b",
    "Tableau": r"\btableau\b",
    "Power BI": r"\bpower bi\b",
    "Machine Learning": r"\bmachine learning\b",
    "AWS": r"\baws\b",
    "Docker": r"\bdocker\b",
    "Git": r"\bgit\b",
    "JavaScript": r"\bjavascript\b",
    "React": r"\breact\b",
    "PostgreSQL": r"\bpostgres\b",
}

def find_skills(text):
    if not text:
        return []
    return [name for name, pat in SKILLS.items()
            if re.search(pat, text, re.IGNORECASE)]

df["skills"] = df["description"].apply(find_skills)

# ── Chart 1: Top skills ────────────────────────
st.subheader("Most In-Demand Skills")

all_skills = [s for lst in df["skills"] for s in lst]
skill_counts = Counter(all_skills)
skill_df = pd.DataFrame(skill_counts.items(), columns=["skill", "count"])
skill_df = skill_df.sort_values("count", ascending=False).head(15)

fig1 = px.bar(
    skill_df,
    x="count", y="skill",
    orientation="h",
    labels={"count": "Number of job postings", "skill": ""},
    color="count",
    color_continuous_scale="Blues",
)
fig1.update_layout(showlegend=False, yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig1, width='stretch')

# ── Chart 2: Salary distribution ──────────────
st.subheader("Salary Ranges")

salary_df = df[df["salary_min"].notna() & df["salary_max"].notna()].copy()
salary_df["salary_mid"] = (salary_df["salary_min"] + salary_df["salary_max"]) / 2

if len(salary_df) > 0:
    fig2 = px.histogram(
        salary_df,
        x="salary_mid",
        nbins=20,
        labels={"salary_mid": "Annual Salary (USD)"},
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Not enough salary data in this dataset yet.")

# ── Raw data table ─────────────────────────────
st.subheader("Browse Jobs")
search = st.text_input("Search by title, company or skill")

if search:
    # Search across title, company AND skills column
    mask = (
        df["title"].str.contains(search, case=False, na=False) |
        df["company"].str.contains(search, case=False, na=False) |
        df["skills"].astype(str).str.contains(search, case=False, na=False)
    )
    results = df[mask]
    st.write(f"Found {len(results)} matching jobs")
    st.dataframe(results[["title", "company", "skills"]])
else:
    st.write(f"Showing all {len(df)} jobs")
    st.dataframe(df[["title", "company", "skills"]])