import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime

# =====================
# SETUP
# =====================
def create_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# =====================
# HELPERS
# =====================
def accept_cookies(driver, wait):
    try:
        btn = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        driver.execute_script("arguments[0].click();", btn)
        print("🍪 Cookies accepted (OneTrust)")
        time.sleep(1)
        return
    except:
        pass

    xpaths = [
        "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'accept')]",
        "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'accept all')]",
        "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'agree')]",
        "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'ok')]",
    ]

    # 1) Try normal page first
    for xpath in xpaths:
        try:
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.execute_script("arguments[0].click();", btn)
            print("🍪 Cookies accepted (main page)")
            time.sleep(1)
            return
        except:
            pass

    # 2) Try inside iframes
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for iframe in iframes:
        try:
            driver.switch_to.frame(iframe)

            for xpath in xpaths:
                try:
                    btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    driver.execute_script("arguments[0].click();", btn)
                    print("🍪 Cookies accepted (iframe)")
                    time.sleep(1)
                    driver.switch_to.default_content()
                    return
                except:
                    pass

            driver.switch_to.default_content()
        except:
            driver.switch_to.default_content()
            continue

    print("⚠️ Cookies button not found / already accepted")


def extract_jobs(driver, container_selector):
    jobs = []
    elements = driver.find_elements(By.CSS_SELECTOR, container_selector)

    for el in elements:
        try:
            links = el.find_elements(By.TAG_NAME, "a")

            for link_el in links:
                link = link_el.get_attribute("href")
                title = link_el.text.strip()

                if not link:
                    continue

                # filter only real job offer links
                if "/jobs/" not in link and "/job/" not in link:
                    continue

                if title:
                    jobs.append((title, link))
                    break

        except:
            continue

    return jobs


def scrape_site(driver, wait, site_name, url, selector):
    print(f"\n🌍 START: {site_name}")
    driver.get(url)

    time.sleep(3)

    accept_cookies(driver, wait)

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except TimeoutException:
        print(f"❌ {site_name} page did not load")
        return []

    time.sleep(2)

    jobs = extract_jobs(driver, selector)
    print(f"✅ Found {len(jobs)} jobs on {site_name}")

    jobs_with_source = [(site_name, title, link) for (title, link) in jobs]
    return jobs_with_source


def remove_duplicates(jobs):
    seen = set()
    unique = []

    for job in jobs:
        source, title, link = job
        if link not in seen:
            seen.add(link)
            unique.append(job)

    return unique


# =====================
# MAIN
# =====================
def main():
    driver = create_driver()
    wait = WebDriverWait(driver, 12)

    try:
        all_jobs = []

        all_jobs += scrape_site(
            driver,
            wait,
            "CWJobs",
            "https://www.cwjobs.co.uk/jobs/java",
            "article, .job, .job-item"
        )

        all_jobs += scrape_site(
            driver,
            wait,
            "Reed",
            "https://www.reed.co.uk/jobs/java-jobs",
            "article, .job-result, .job"
        )

        all_jobs = remove_duplicates(all_jobs)

        # SAVE
        filename = f"jobs_output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Source", "Title", "Link"])

            for job in all_jobs:
                writer.writerow(job)

        print(f"\n✅ Saved {len(all_jobs)} unique jobs to {filename}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()