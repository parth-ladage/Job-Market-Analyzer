from serpapi import GoogleSearch
import pandas as pd

def fetch_jobs(query="Data Analyst", location="India", num_results=30):
    params = {
        "engine": "google_jobs",
        "q": f"{query} in {location}",
        "hl": "en",
        "api_key": "d8762964afd6f7425253ec3e7ce4e794daf3eba5f5d0e84ed678129d267e6c2c",  # Replace if needed
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # 🔍 DEBUG: Print raw response keys
    print("Available keys in result:", results.keys())

    # 🔍 DEBUG: Print raw job results if present
    job_list = results.get("jobs_results", [])
    print(f"Found {len(job_list)} jobs")

    # ✅ Build DataFrame
    jobs = []
    for job in job_list[:num_results]:
        jobs.append({
            "Title": job.get("title"),
            "Company": job.get("company_name"),
            "Location": job.get("location"),
            "Posted": job.get("detected_extensions", {}).get("posted_at"),
            "Description": job.get("description"),
            "Link": job.get("job_highlighted_url") or job.get("via") or ""
        })

    return pd.DataFrame(jobs)

if __name__ == "__main__":
    df = fetch_jobs()
    print(df.head())
    df.to_csv("../data/serpapi_indeed_jobs.csv", index=False)
    print("✅ Data saved to data/serpapi_indeed_jobs.csv")
