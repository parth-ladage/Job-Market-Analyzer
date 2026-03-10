# 💼 Data Science Job Market Analyzer

A comprehensive Python-based tool to scrape, analyze, and visualize data science job listings. This project extracts job data from platforms like LinkedIn and Indeed, processes it to find the most in-demand skills, and presents the insights through an interactive Streamlit dashboard.

## ✨ Features

- **Automated Job Scraping:** Uses SerpAPI and Google Search to fetch real-time job postings from LinkedIn and Indeed.
- **Skill Extraction:** Automatically scans job descriptions to identify required skills (e.g., Python, SQL, Machine Learning, AWS).
- **Interactive Dashboard:** A dynamic Streamlit frontend to visualize data.
- **Filtering Capabilities:** Filter jobs by specific skills, locations, or platforms.
- **Market Insights:** Visualizes the top 15 most in-demand skills and job posting trends over time.
- **Data Export:** Download the filtered job market data as a CSV directly from the dashboard.

## 🛠️ Tech Stack

- **Frontend:** Streamlit, Plotly (for interactive charts)
- **Backend/Data Processing:** Python, Pandas, NumPy
- **Data Scraping:** `google-search-results` (SerpAPI), `beautifulsoup4`
- **Other Tools:** NLTK, Matplotlib, Seaborn

## 🚀 How to Run the Project

Follow these steps to set up and run the Job Market Analyzer on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/parth-ladage/Job-Market-Analyzer.git
cd Job-Market-Analyzer
```

### 2. Set Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.
**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Run the Dashboard

Start the Streamlit application:

```bash
streamlit run dashboard.py
```

This will automatically open the dashboard in your default web browser (usually at `http://localhost:8501`).

## 📁 Project Structure

```text
Job_Market_Analyzer/
│
├── dashboard.py           # Main Streamlit dashboard script
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore file (excludes venv/, data/, etc.)
├── README.md              # Project documentation
│
└── src/                   # Source code for scrapers and utilities
    ├── job_fetcher.py     # Main script to fetch jobs via SerpAPI
    ├── scraper.py         # Additional scraping logic
    └── ...
```

## ⚙️ Configuration

- **API Keys:** The project uses SerpAPI to fetch jobs. Ensure you have your SerpAPI key configured in `src/job_fetcher.py` (or load it securely via a `.env` file).

## 👤 Author

**Parth Ladage**

- GitHub: [@parth-ladage](https://github.com/parth-ladage)
