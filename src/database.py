import sqlite3
import json
import glob
from datetime import datetime

def create_database():
    # This creates jobs.db file in your data folder
    conn = sqlite3.connect(r"C:\Users\HP\job_market_tracker\data\jobs.db")
    cursor = conn.cursor()
    
    # Create jobs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            description TEXT,
            salary_min REAL,
            salary_max REAL,
            date_posted TEXT,
            source TEXT,
            scraped_date TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database created successfully!")

def save_jobs_to_db(jobs):
    conn = sqlite3.connect(r"C:\Users\HP\job_market_tracker\data\jobs.db")
    cursor = conn.cursor()
    
    new_jobs = 0
    duplicate_jobs = 0
    
    for job in jobs:
        # Check if job already exists
        # So we don't save the same job twice
        cursor.execute("""
            SELECT id FROM jobs 
            WHERE title = ? AND company = ?
        """, (job.get("title"), job.get("company")))
        
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("""
                INSERT INTO jobs 
                (title, company, location, description, 
                salary_min, salary_max, date_posted, source, scraped_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                job.get("title", ""),
                job.get("company", ""),
                job.get("location", ""),
                job.get("description", ""),
                job.get("salary_min"),
                job.get("salary_max"),
                job.get("date", ""),
                job.get("source", ""),
                datetime.now().strftime("%Y-%m-%d")
            ))
            new_jobs += 1
        else:
            duplicate_jobs += 1
    
    conn.commit()
    conn.close()
    print(f"Saved {new_jobs} new jobs — skipped {duplicate_jobs} duplicates")

def load_jobs_from_db():
    import pandas as pd
    conn = sqlite3.connect(r"C:\Users\HP\job_market_tracker\data\jobs.db")
    df = pd.read_sql_query("SELECT * FROM jobs", conn)
    conn.close()
    print(f"Loaded {len(df)} jobs from database")
    return df

if __name__ == "__main__":
    create_database()
    print("Database ready!")