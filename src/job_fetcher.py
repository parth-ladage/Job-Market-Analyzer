from serpapi import GoogleSearch
import pandas as pd
import os

# ✅ Ensure 'data/' directory exists
os.makedirs("data", exist_ok=True)

# ✅ Define common skills list
skills_list = [
    "Python", "R", "SQL", "Java", "C++", "Tableau", "Power BI", "Excel",
    "AWS", "GCP", "Azure", "Spark", "Hadoop", "Scikit-learn", "TensorFlow",
    "Keras", "PyTorch", "NLP", "Pandas", "NumPy", "Matplotlib", "Seaborn",
    "Docker", "Git", "Machine Learning", "Deep Learning", "Flask", "FastAPI"
]

def extract_skills_from_description(description, skills):
    return ", ".join([skill for skill in skills if skill.lower() in description.lower()])

def clean_jobs(job_list):
    jobs = []
    for job in job_list:
        jobs.append({
            "Title": job.get("title", "N/A"),
            "Company": job.get("company_name", "N/A"),
            "Location": job.get("location", "N/A"),
            "Posted": job.get("detected_extensions", {}).get("posted_at", "Unknown"),
            "Description": job.get("description", ""),  # Ensure default is an empty string
            "Link": job.get("job_highlighted_url") or job.get("via") or ""
        })
    return jobs

def fetch_jobs_from_linkedin(query="Data Scientist", location="India", num_results=30):
    params = {
        "engine": "google_jobs",
        "q": f"{query} in {location}",
        "hl": "en",
        "api_key": os.getenv("SERPAPI_API_KEY"),
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    job_list = results.get("jobs_results", [])[:num_results]
    print(f"🔍 {len(job_list)} jobs fetched from LinkedIn")

    jobs = clean_jobs(job_list)
    df = pd.DataFrame(jobs)

    # Ensure all necessary columns exist
    for col in ["Title", "Company", "Location", "Posted", "Description", "Link"]:
        if col not in df.columns:
            df[col] = "N/A"


    if "Description" not in df.columns:
        df["Description"] = ""

    df["Platform"] = "LinkedIn"
    df["Matched Skills"] = df["Description"].apply(lambda d: extract_skills_from_description(d or "", skills_list))

    df.to_csv("data/serpapi_linkedin_jobs.csv", index=False)
    print("✅ LinkedIn jobs saved.")
    return df

def fetch_jobs_from_indeed(query="Data Scientist", location="India", num_results=30):
    params = {
        "engine": "google_jobs",
        "q": f"{query} in {location}",
        "hl": "en",
        "api_key": "d8762964afd6f7425253ec3e7ce4e794daf3eba5f5d0e84ed678129d267e6c2c",
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    job_list = results.get("jobs_results", [])[:num_results]
    print(f"🔍 {len(job_list)} jobs fetched from Indeed")

    jobs = clean_jobs(job_list)
    df = pd.DataFrame(jobs)

    # Ensure all necessary columns exist
    for col in ["Title", "Company", "Location", "Posted", "Description", "Link"]:
        if col not in df.columns:
            df[col] = "N/A"


    if "Description" not in df.columns:
        df["Description"] = ""

    df["Platform"] = "Indeed"
    df["Matched Skills"] = df["Description"].apply(lambda d: extract_skills_from_description(d or "", skills_list))

    df.to_csv("data/serpapi_indeed_jobs.csv", index=False)
    print("✅ Indeed jobs saved.")
    return df

# ✅ Unified fetcher
def fetch_all_jobs():
    linkedin_df = fetch_jobs_from_linkedin()
    indeed_df = fetch_jobs_from_indeed()
    combined = pd.concat([linkedin_df, indeed_df], ignore_index=True)
    return combined
