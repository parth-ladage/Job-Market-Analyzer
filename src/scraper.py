from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

def fetch_naukri_jobs(query="data scientist", location="India"):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    import urllib.parse

    query_encoded = urllib.parse.quote(query)
    location_encoded = urllib.parse.quote(location)
    url = f"https://www.naukri.com/{query_encoded}-jobs-in-{location_encoded}"

    options = Options()
    options.add_argument("--headless")  # comment this to see browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)  # wait for JS to render
    with open("naukri_rendered_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)


    job_cards = driver.find_elements(By.CSS_SELECTOR, "div.styles_jlc__main__nkkgU")  # ✅ verified selector

    jobs = []
    for card in job_cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "a.styles_jlc__jobTitle__rT3fV").text
            company = card.find_element(By.CSS_SELECTOR, "a.styles_jlc__companyName__RzHn4").text
            location = card.find_element(By.CSS_SELECTOR, "span.styles_jlc__location__nWotf").text
            experience = card.find_element(By.CSS_SELECTOR, "span.styles_jlc__experience__3cL_v").text
            skills = card.find_element(By.CSS_SELECTOR, "div.styles_jlc__skills__BzFYU").text

            jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Experience": experience,
                "Skills": skills
            })
        except:
            continue

    driver.quit()
    return pd.DataFrame(jobs)


if __name__ == "__main__":
    df = fetch_naukri_jobs()
    print(df.head())
    df.to_csv("../data/naukri_data_science_jobs.csv", index=False)
    print("✅ Data saved to data/naukri_data_science_jobs.csv")
