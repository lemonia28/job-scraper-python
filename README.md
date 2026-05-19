# Job Scraper Bot (Python + Selenium)

A simple **job scraping automation tool** written in **Python** using **Selenium WebDriver**.

The script collects job offers from popular UK job portals and exports results into a timestamped **CSV file**, including job title, link, and source website.

---

## Features

- Scrapes job offers from:
  - **CWJobs**
  - **Reed**
- Extracts:
  - Job title
  - Job link
  - Source website
- Saves output to CSV with timestamp (prevents overwrite errors)
- Removes duplicate job links automatically

---

## Output Example

The script generates files like:
jobs_output_2026-05-19_15-19-24.csv


CSV structure:

| Source | Title | Link |
|--------|-------|------|
| Reed   | Python Developer | https://... |
| CWJobs | Junior Python Engineer | https://... |

---

## Requirements

- Python 3.10+
- Google Chrome installed
- Selenium

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/job-scraper-python.git
cd job-scraper-python

Install dependencies:
pip install -r requirements.txt

Run
python scraper.py

After running, a new CSV file will be created in the project folder.

Notes

Some websites may display cookie banners or anti-bot protections.
This script is intended as a portfolio automation project and may require updates if website layouts change.

Possible Improvements
Add support for multiple pages of results
Add keyword filtering from command-line arguments
Save results to a database (SQLite)
Add automatic detection of new jobs since last run
Add headless mode
Author

Created by Monika Wolniewicz

License

This project is open-source and available under the MIT License.