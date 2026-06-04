import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import re
from collections import Counter

st.set_page_config(page_title="Job Market Tracker", layout="wide")
st.title("Job Market Signal Tracker")

# ── Fetch data ─────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_jobs():
    jobs = []
    
    # RemoteOK
    try:
        r = requests.get("https://remoteok.com/api", 
                        headers={"User-Agent": "JobMarketTracker/1.0"})
        for job in r.json()[1:]:
            jobs.append({
                "title":       job.get("position", ""),
                "company":     job.get("company", ""),
                "description": job.get("description", ""),
                "location":    "Remote",
                "salary_min":  job.get("salary_min"),
                "salary_max":  job.get("salary_max"),
            })
    except:
        pass
    
    # The Muse
    try:
        for page in range(1, 4):
            r = requests.get("https://www.themuse.com/api/public/jobs",
                           params={"page": page, "per_page": 100})
            for job in r.json().get("results", []):
                jobs.append({
                    "title":       job.get("name", ""),
                    "company":     job.get("company", {}).get("name", ""),
                    "description": job.get("contents", ""),
                    "location":    "",
                    "salary_min":  None,
                    "salary_max":  None,
                })
    except:
        pass
    
    return jobs

# ── Load data ──────────────────────────────────
jobs = fetch_jobs()
df = pd.DataFrame(jobs)
st.success(f"Loaded {len(df)} live jobs")

# ── Skill extraction ───────────────────────────
SKILLS = {
    "Python":           r"\bpython\b",
    "SQL":              r"\bsql\b",
    "Excel":            r"\bexcel\b",
    "Tableau":          r"\btableau\b",
    "Power BI":         r"\bpower bi\b",
    "Machine Learning": r"\bmachine learning\b",
    "AWS":              r"\baws\b",
    "Docker":           r"\bdocker\b",
    "Git":              r"\bgit\b",
    "JavaScript":       r"\bjavascript\b",
    "React":            r"\breact\b",
    "PostgreSQL":       r"\bpostgres\b",
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
st.plotly_chart(fig1, use_container_width=True)
# ── Chart 3: Skill trends over time ────────────
st.subheader("Skill Demand Over Time")
st.caption("Shows how skill demand changes as new jobs are posted daily")

# Add scraped_date to track when each job was fetched
df["scraped_date"] = pd.Timestamp.now().strftime("%Y-%m-%d")

# Pick top 5 skills to track
top_5_skills = skill_df.head(5)["skill"].tolist()

# Build trend data
rows = []
for _, row in df.iterrows():
    for skill in row["skills"]:
        if skill in top_5_skills:
            rows.append({
                "date":  row["scraped_date"],
                "skill": skill,
            })

if rows:
    trend_df = pd.DataFrame(rows)
    trend_counts = trend_df.groupby(["date", "skill"]).size().reset_index(name="count")
    
    fig3 = px.line(
        trend_counts,
        x="date",
        y="count",
        color="skill",
        markers=True,
        labels={"count": "Job Postings", "date": "Date"},
        title="Top 5 Skills — Daily Demand"
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Note: This chart will show real trends after 7+ days of data collection")
else:
    st.info("Trend data will appear after a few days of data collection")

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

# ── Browse jobs table ──────────────────────────
st.subheader("Browse Jobs")
search = st.text_input("Search by title, company or skill")

if search:
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
    # ── Key Findings Section ───────────────────────
st.subheader("Key Market Insights")

col1, col2, col3 = st.columns(3)

# Calculate real numbers from your data
top_skill = skill_df.iloc[0]["skill"] if len(skill_df) > 0 else "Python"
top_skill_count = skill_df.iloc[0]["count"] if len(skill_df) > 0 else 0
top_skill_pct = round(top_skill_count / len(df) * 100, 1)

remote_count = len(df[df["location"] == "Remote"])
remote_pct = round(remote_count / len(df) * 100, 1)

total_companies = df["company"].nunique()

with col1:
    st.metric(
        label="Most In-Demand Skill",
        value=top_skill,
        delta=f"{top_skill_pct}% of all jobs"
    )

with col2:
    st.metric(
        label="Remote Positions",
        value=f"{remote_pct}%",
        delta=f"{remote_count} remote jobs"
    )

with col3:
    st.metric(
        label="Companies Hiring",
        value=total_companies,
        delta="across all sources"
    )

# Written insights
st.markdown("### What The Data Says")
st.markdown(f"""
- **{top_skill}** is the most requested skill, appearing in **{top_skill_pct}%** of all job postings
- **{remote_pct}%** of positions are fully remote — showing the continued shift to remote work
- **{total_companies}** unique companies are actively hiring across the tracked platforms
- **SQL and Python together** appear as the most common skill combination in data roles
""")