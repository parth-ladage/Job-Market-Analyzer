import streamlit as st
import pandas as pd
import plotly.express as px
from src.job_fetcher import fetch_all_jobs, extract_skills_from_description, skills_list
from datetime import datetime, timedelta
from collections import Counter

st.set_page_config(page_title="Job Market Analyzer", layout="wide")
st.title("💼 Data Science Job Market Analyzer")

# Load data
with st.spinner("Fetching job data..."):
    df = fetch_all_jobs()
st.success("Job data loaded successfully!")

# Skill Extraction
df["Matched Skills"] = df["Description"].apply(
    lambda desc: extract_skills_from_description(desc or "", skills_list)
)

# Convert "Posted" column to datetime safely
relative_dates = {
    "today": 0,
    "1 day ago": 1,
    "2 days ago": 2,
    "3 days ago": 3,
    "4 days ago": 4,
    "5 days ago": 5,
    "6 days ago": 6,
    "1 week ago": 7,
    "2 weeks ago": 14,
    "3 weeks ago": 21
}

def convert_to_date(relative_date):
    days_ago = relative_dates.get(str(relative_date).lower(), None)
    if days_ago is not None:
        return datetime.now() - timedelta(days=days_ago)
    return None

if "Posted" in df.columns and df["Posted"].notna().any():
    df["Posted Date"] = df["Posted"].apply(convert_to_date)
else:
    df["Posted Date"] = pd.NaT

# Sidebar Filters
skills = sorted(set(", ".join(df["Matched Skills"].dropna()).split(", ")))
selected_skill = st.sidebar.selectbox("🎯 Filter by Skill", ["All"] + skills)
if selected_skill != "All":
    df = df[df["Matched Skills"].str.contains(selected_skill)]

locations = sorted(df["Location"].dropna().unique())
selected_locations = st.sidebar.multiselect("📍 Filter by Location", locations, default=locations)
if selected_locations:
    df = df[df["Location"].isin(selected_locations)]

platforms = sorted(df["Platform"].dropna().unique())
selected_platforms = st.sidebar.multiselect("🟢 Filter by Platform", platforms, default=platforms)
if selected_platforms:
    df = df[df["Platform"].isin(selected_platforms)]

# Display Table
st.subheader("🔍 Filtered Job Listings")
st.dataframe(df, use_container_width=True)

# Download Button
st.download_button("⬇️ Download CSV", df.to_csv(index=False), "jobs.csv", "text/csv")

# Plot Skill Frequency
skills_flat = ", ".join(df["Matched Skills"]).split(", ")
skill_counts = Counter(skills_flat)
skill_counts.pop('', None)
skill_df = pd.DataFrame(skill_counts.items(), columns=["Skill", "Count"])
skill_df = skill_df.sort_values(by="Count", ascending=False).head(15)

fig = px.bar(skill_df, x="Skill", y="Count", title="Top 15 In-Demand Skills", color="Count", color_continuous_scale="Blues")
st.plotly_chart(fig, use_container_width=True)

# 📈 Time Trend Chart
if df["Posted Date"].notna().any():
    trend_df = df.dropna(subset=["Posted Date"])
    trend_df["Posted Date"] = trend_df["Posted Date"].dt.date
    count_by_date = trend_df.groupby("Posted Date").size().reset_index(name="Job Count")

    line_chart = px.line(count_by_date, x="Posted Date", y="Job Count",
                         title="📅 Job Posting Trend Over Time",
                         markers=True)
    st.plotly_chart(line_chart, use_container_width=True)
else:
    st.info("No valid 'Posted' dates available to generate trend chart.")
