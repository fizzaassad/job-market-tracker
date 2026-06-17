import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime

load_dotenv(override=False)  # won't crash if .env doesn't exist

def get_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("Supabase credentials not found!")
    
    return create_client(url, key)

def save_jobs_to_db(jobs):
    supabase = get_client()
    
    new_jobs = 0
    duplicate_jobs = 0
    
    for job in jobs:
        # Check if job already exists
        existing = supabase.table("jobs")\
            .select("id")\
            .eq("title", job.get("title", ""))\
            .eq("company", job.get("company", ""))\
            .execute()
        
        if not existing.data:
            supabase.table("jobs").insert({
                "title":        job.get("title", ""),
                "company":      job.get("company", ""),
                "location":     job.get("location", ""),
                "description":  job.get("description", ""),
                "salary_min":   job.get("salary_min"),
                "salary_max":   job.get("salary_max"),
                "date_posted":  job.get("date", ""),
                "source":       job.get("source", ""),
                "scraped_date": datetime.now().strftime("%Y-%m-%d")
            }).execute()
            new_jobs += 1
        else:
            duplicate_jobs += 1
    
    print(f"Saved {new_jobs} new jobs — skipped {duplicate_jobs} duplicates")

def load_jobs_from_db():
    import pandas as pd
    supabase = get_client()
    response = supabase.table("jobs").select("*").execute()
    df = pd.DataFrame(response.data)
    print(f"Loaded {len(df)} jobs from Supabase")
    return df

if __name__ == "__main__":
    print("Testing Supabase connection...")
    supabase = get_client()
    response = supabase.table("jobs").select("count", count="exact").execute()
    print(f"Jobs in database: {response.count}")