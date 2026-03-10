from serpapi import GoogleSearch
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# Define skill keywords
skills_list = [
    "Python", "R", "SQL", "Java", "C++", "Tableau", "Power BI", "Excel",
    "AWS", "GCP", "Azure", "Spark", "Hadoop", "Scikit-learn", "TensorFlow",
    "Keras", "PyTorch", "NLP", "Pandas", "NumPy", "Matplotlib", "Seaborn",
    "Docker", "Git", "Machine Learning", "Deep Learning", "Flask", "FastAPI"
]

def fetch_jobs(query="Data Scientist", location="India", num_results=30):
    params = {
        "engine": "google_jobs",
        "q": f"{query} in {location}",
        "hl": "en",
        "api_key": "d8762964afd6f7425253ec3e7ce4e794daf3eba5f5d0e84ed678129d267e6c2c",  # Replace with your key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    job_list = results.get("jobs_results", [])[:num_results]
    jobs = []
    for job in job_list:
        jobs.append({
            "Title": job.get("title"),
            "Company": job.get("company_name"),
            "Location": job.get("location"),
            "Posted": job.get("detected_extensions", {}).get("posted_at"),
            "Description": job.get("description"),
            "Link": job.get("job_highlighted_url") or job.get("via") or ""
        })

    df = pd.DataFrame(jobs)
    return df

def extract_skills_from_description(description, skills):
    return ", ".join([skill for skill in skills if skill.lower() in description.lower()])

# Main logic
if __name__ == "__main__":
    df = fetch_jobs()
    df["Matched Skills"] = df["Description"].apply(
        lambda desc: extract_skills_from_description(desc or "", skills_list)
    )

    df.to_csv("../data/serpapi_linkedin_jobs.csv", index=False)
    print("✅ Data saved to data/serpapi_linkedin_jobs.csv")
    print(df.head())

    # Count skills
    skills_flat = ", ".join(df["Matched Skills"]).split(", ")
    skill_counts = Counter(skills_flat)
    skill_counts.pop('', None)  # Clean empty entries

    # Print top 10
    print("🔥 Top 10 Skills:")
    for skill, count in skill_counts.most_common(10):
        print(f"{skill}: {count}")

    # Visualize
    plt.figure(figsize=(10, 5))
    plt.bar(skill_counts.keys(), skill_counts.values(), color="skyblue")
    plt.xticks(rotation=45, ha="right")
    plt.title("Top Skills in Data Science Job Descriptions")
    plt.tight_layout()
    plt.show()
