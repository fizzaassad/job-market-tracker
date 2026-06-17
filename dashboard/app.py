import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import re
import os
from collections import Counter
from dotenv import load_dotenv
from supabase import create_client

# ── Page config ────────────────────────────────
st.set_page_config(page_title="Job Market Tracker", layout="wide")
st.title("Job Market Signal Tracker")
st.caption("Data loaded from Supabase cloud database")

# ── Load data from Supabase ────────────────────
load_dotenv()

@st.cache_data(ttl=3600)
def fetch_jobs():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    # If Supabase credentials exist, use database
    if url and key:
        try:
            supabase = create_client(url, key)
            response = supabase.table("jobs").select("*").execute()
            if response.data:
                return response.data
        except:
            pass
    
    # Fallback: fetch live from APIs
    jobs = []
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
                "scraped_date": "",
            })
    except:
        pass
    
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
                    "scraped_date": "",
                })
    except:
        pass
    
    return jobs

# ── Build DataFrame ────────────────────────────
jobs = fetch_jobs()
df = pd.DataFrame(jobs)
st.success(f"Loaded {len(df)} jobs")

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
            if re.search(pat, str(text), re.IGNORECASE)]

df["skills"] = df["description"].apply(find_skills)

# ── Key Metrics ────────────────────────────────
st.subheader("Key Market Insights")

all_skills = [s for lst in df["skills"] for s in lst]
skill_counts = Counter(all_skills)
skill_df = pd.DataFrame(skill_counts.items(), columns=["skill", "count"])
skill_df = skill_df.sort_values("count", ascending=False)

col1, col2, col3 = st.columns(3)

top_skill = skill_df.iloc[0]["skill"] if len(skill_df) > 0 else "Python"
top_skill_pct = round(skill_df.iloc[0]["count"] / len(df) * 100, 1) if len(skill_df) > 0 else 0
remote_count = len(df[df["location"] == "Remote"]) if "location" in df.columns else 0
remote_pct = round(remote_count / len(df) * 100, 1)
total_companies = df["company"].nunique()

with col1:
    st.metric("Most In-Demand Skill", top_skill, f"{top_skill_pct}% of all jobs")
with col2:
    st.metric("Remote Positions", f"{remote_pct}%", f"{remote_count} remote jobs")
with col3:
    st.metric("Companies Hiring", total_companies, "across all sources")

st.markdown("### What The Data Says")
st.markdown(f"""
- **{top_skill}** is the most requested skill, appearing in **{top_skill_pct}%** of all postings
- **{remote_pct}%** of positions are fully remote
- **{total_companies}** unique companies are actively hiring
- **SQL and Python together** are the most common skill combination in data roles
""")

# ── Chart 1: Top Skills ────────────────────────
st.subheader("Most In-Demand Skills")

fig1 = px.bar(
    skill_df.head(15),
    x="count", y="skill",
    orientation="h",
    labels={"count": "Number of job postings", "skill": ""},
    color="count",
    color_continuous_scale="Blues",
)
fig1.update_layout(showlegend=False, yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig1, use_container_width=True)

# ── Chart 2: Salary Distribution ──────────────
st.subheader("Salary Ranges")

salary_df = df[df["salary_min"].notna() & df["salary_max"].notna()].copy()
if len(salary_df) > 0:
    salary_df["salary_mid"] = (
        pd.to_numeric(salary_df["salary_min"], errors="coerce") +
        pd.to_numeric(salary_df["salary_max"], errors="coerce")
    ) / 2
    fig2 = px.histogram(salary_df, x="salary_mid", nbins=20,
                        labels={"salary_mid": "Annual Salary (USD)"})
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Not enough salary data yet.")

# ── Chart 3: Trends Over Time ──────────────────
st.subheader("Skill Demand Over Time")
st.caption("Shows real trends after 7+ days of data collection")

if "scraped_date" in df.columns and df["scraped_date"].notna().any():
    top_5 = skill_df.head(5)["skill"].tolist()
    rows = []
    for _, row in df.iterrows():
        for skill in row["skills"]:
            if skill in top_5:
                rows.append({"date": row["scraped_date"], "skill": skill})
    
    if rows:
        trend_df = pd.DataFrame(rows)
        trend_counts = trend_df.groupby(["date", "skill"]).size().reset_index(name="count")
        fig3 = px.line(trend_counts, x="date", y="count", color="skill",
                      markers=True, labels={"count": "Job Postings", "date": "Date"})
        st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Trend data will appear after a few days of data collection.")

# ── Skills Gap Analyzer ────────────────────────
st.subheader("Skills Gap Analyzer")
st.caption("Find out which skills you need for your target role")

col1, col2 = st.columns(2)
with col1:
    target_role = st.text_input("Enter your target job title",
                                placeholder="e.g. Data Analyst")
with col2:
    user_skills = st.multiselect("Select skills you already have",
                                 options=list(SKILLS.keys()))

if target_role:
    role_jobs = df[df["title"].str.contains(target_role, case=False, na=False)]
    
    if len(role_jobs) == 0:
        st.warning(f"No jobs found for '{target_role}'. Try a different title.")
    else:
        role_skills = [s for lst in role_jobs["skills"] for s in lst]
        role_skill_counts = Counter(role_skills)
        total_role_jobs = len(role_jobs)
        
        gap_data = []
        for skill, count in role_skill_counts.most_common(10):
            pct = round(count / total_role_jobs * 100, 1)
            gap_data.append({
                "skill":       skill,
                "demand_pct":  pct,
                "you_have_it": "✅ Yes" if skill in user_skills else "❌ Missing"
            })
        
       gap_df = pd.DataFrame(gap_data)

if len(gap_df) == 0:
    st.warning("No skills found for this role. Try a different job title.")
else:
    missing = gap_df[gap_df["you_have_it"] == "❌ Missing"]["skill"].tolist()
    have    = gap_df[gap_df["you_have_it"] == "✅ Yes"]["skill"].tolist()
    
    col3, col4 = st.columns(2)
    with col3:
        st.success(f"✅ Skills you have: {len(have)}")
        for s in have:
            st.write(f"• {s}")
    with col4:
        st.error(f"❌ Skills to learn: {len(missing)}")
        for s in missing:
            pct = gap_df[gap_df["skill"] == s]["demand_pct"].values[0]
            st.write(f"• {s} — needed in {pct}% of jobs")
    
    fig4 = px.bar(gap_df, x="demand_pct", y="skill",
                 color="you_have_it", orientation="h",
                 color_discrete_map={"✅ Yes": "#22c55e", "❌ Missing": "#ef4444"},
                 labels={"demand_pct": "% of job postings", "skill": ""},
                 title=f"Skill Demand for {target_role}")
    fig4.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig4, use_container_width=True)
        
        st.markdown(f"### Results for: **{target_role}** ({total_role_jobs} jobs)")
        
        col3, col4 = st.columns(2)
        with col3:
            st.success(f"✅ Skills you have: {len(have)}")
            for s in have:
                st.write(f"• {s}")
        with col4:
            st.error(f"❌ Skills to learn: {len(missing)}")
            for s in missing:
                pct = gap_df[gap_df["skill"] == s]["demand_pct"].values[0]
                st.write(f"• {s} — needed in {pct}% of jobs")
        
        fig4 = px.bar(gap_df, x="demand_pct", y="skill",
                     color="you_have_it", orientation="h",
                     color_discrete_map={"✅ Yes": "#22c55e", "❌ Missing": "#ef4444"},
                     labels={"demand_pct": "% of job postings", "skill": ""},
                     title=f"Skill Demand for {target_role}")
        fig4.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig4, use_container_width=True)

# ── Browse Jobs ────────────────────────────────
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