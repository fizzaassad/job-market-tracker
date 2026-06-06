from database import save_jobs_to_db
import requests
import json
from datetime import datetime
def fetch_remoteok():
    response = requests.get(
        "https://remoteok.com/api",
        headers={"User-Agent": "JobMarketTracker/1.0"}
    )
    jobs = response.json()[1:]
    
    clean_jobs = []
    for job in jobs:
        clean_jobs.append({
            "title":      job.get("position", ""),
            "company":    job.get("company", ""),
            "location":   "Remote",
            "description": job.get("description", ""),
            "tags":       job.get("tags", []),
            "date":       job.get("date", ""),
            "salary_min": job.get("salary_min", None),
            "salary_max": job.get("salary_max", None),
        })
    
    print(f"RemoteOK: got {len(clean_jobs)} jobs")
    return clean_jobs
# Fetch jobs
response = requests.get(
    "https://remoteok.com/api",
    headers={"User-Agent": "JobMarketTracker/1.0"}
)
jobs = response.json()[1:]  # skip first metadata item

# Keep only the fields we care about
clean_jobs = []

for job in jobs:
    clean_jobs.append({
        "title":       job.get("position", ""),
        "company":     job.get("company", ""),
        "location":    "Remote",
        "description": job.get("description", ""),
        "tags":        job.get("tags", []),
        "date":        job.get("date", ""),
        "salary_min":  job.get("salary_min", None),
        "salary_max":  job.get("salary_max", None),
    })

# Save to a file with today's date in the name
today = datetime.now().strftime("%Y-%m-%d")
filename = r"C:\Users\HP\job_market_tracker\data\jobs_{}.json".format(today)

with open(filename, "w") as f:
    json.dump(clean_jobs, f, indent=2)

print(f"Saved {len(clean_jobs)} jobs to {filename}")
def fetch_the_muse():
    jobs = []
    
    for page in range(1, 6):  # gets 5 pages = ~500 jobs
        response = requests.get(
            "https://www.themuse.com/api/public/jobs",
            params={"page": page, "per_page": 100}
        )
        data = response.json()
        
        for job in data.get("results", []):
            jobs.append({
                "title":       job.get("name", ""),
                "company":     job.get("company", {}).get("name", ""),
                "location":    ", ".join([l["name"] for l in job.get("locations", [])]),
                "description": job.get("contents", ""),
                "tags":        [c["name"] for c in job.get("categories", [])],
                "date":        job.get("publication_date", ""),
                "salary_min":  None,
                "salary_max":  None,
            })
        
        print(f"Fetched page {page} from The Muse — {len(jobs)} jobs so far")
        time.sleep(0.5)  # be polite, don't spam their server
    
    return jobs
import time

# Collect from both sources
remoteok_jobs = fetch_remoteok()      # your existing function
muse_jobs     = fetch_the_muse()      # new function

# Combine into one list
all_jobs = remoteok_jobs + muse_jobs

print(f"Total: {len(all_jobs)} jobs from both sources")

# Save as usual
today = datetime.now().strftime("%Y-%m-%d")
filename = r"C:\Users\HP\job_market_tracker\data\jobs_{}.json".format(today)
# Save to JSON (keep this as backup)
with open(filename, "w") as f:
    json.dump(all_jobs, f, indent=2)

# Save to database (new)

save_jobs_to_db(all_jobs)
    