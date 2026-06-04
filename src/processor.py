import pandas as pd
import json
import glob
import re
# Load the most recent data file
files = glob.glob("../data/jobs_*.json")
latest_file = sorted(files)[-1]  # gets the most recent one

print(f"Loading: {latest_file}")

with open(latest_file) as f:
    jobs = json.load(f)

# Convert list of dictionaries → a table (DataFrame)
df = pd.DataFrame(jobs)

# Look at what we have
print(df.shape)        # (rows, columns)
print(df.columns)      # column names
print(df.head(3))      # first 3 rows

# Dictionary of skills and their search patterns
# \b means "word boundary" — so "sql" won't match "mysql" accidentally
SKILLS = {
    "Python":       r"\bpython\b",
    "SQL":          r"\bsql\b",
    "Excel":        r"\bexcel\b",
    "Tableau":      r"\btableau\b",
    "Power BI":     r"\bpower bi\b",
    "Machine Learning": r"\bmachine learning\b",
    "AWS":          r"\baws\b",
    "Docker":       r"\bdocker\b",
    "Git":          r"\bgit\b",
    "JavaScript":   r"\bjavascript\b",
    "React":        r"\breact\b",
    "PostgreSQL":   r"\bpostgres\b",
}

def find_skills(text):
    """Look through a job description and return which skills it mentions."""
    if not text:
        return []

    text = text.lower()  # make everything lowercase so Python == python
    found = []

    for skill_name, pattern in SKILLS.items():
        if re.search(pattern, text, re.IGNORECASE):
            found.append(skill_name)

    return found

# Apply to every job — this creates a new column called "skills"
df["skills"] = df["description"].apply(find_skills)

# See the result
print("\nSkills found in first 5 jobs:")
for i, row in df.head(5).iterrows():
    print(f"  {row['title']}: {row['skills']}")
    from collections import Counter

# Flatten all skill lists into one big list
all_skills = []
for skill_list in df["skills"]:
    all_skills.extend(skill_list)

# Count each skill
skill_counts = Counter(all_skills)

# Convert to a DataFrame for easier analysis
skill_df = pd.DataFrame(
    skill_counts.items(),
    columns=["skill", "count"]
)
skill_df = skill_df.sort_values("count", ascending=False)

# Calculate what % of jobs mention each skill
total_jobs = len(df)
skill_df["percent_of_jobs"] = (skill_df["count"] / total_jobs * 100).round(1)

print("\n=== TOP SKILLS IN DEMAND ===")
print(skill_df.head(10).to_string(index=False))