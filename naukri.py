# scrape_naukri.py
import re
import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_naukri(text1):
    base_url = "https://www.naukri.com/"
    url = base_url + f"{text1}-jobs"

    opts = Options()

    driver = webdriver.Chrome(options=opts)
    driver.get(url)

    scraper = cloudscraper.create_scraper()

    # Wait for the page to be fully loaded
    wait = WebDriverWait(driver, 40)  # Adjust the timeout as needed
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_jlc__main__VdwtF')))

    bs = BeautifulSoup(driver.page_source, "html.parser")

    job_list = bs.find('div', {'class': 'styles_job-listing-container__OCfZC'})
    jobs = job_list.find_all('div', {'class': 'srp-jobtuple-wrapper'})

    info_naukri = []

    for job in jobs:
        TITLE = job.find('a', {'class': 'title'})
        title = TITLE.text
        url = TITLE['href']
        company_name = job.find('a', {'class': 'comp-name'}).text

        # Check if the 'locWdth' element is present
        location_element = job.find('span', {'class': 'locWdth'})
        company_location = location_element.text if location_element else 'N/A'

        cskills_list = [tag.text for tag in job.find_all('li', {'class': 'dot-gt tag-li'})]
        cskills = ', '.join(cskills_list)

        data = {
            'title': title,
            'company name': company_name,
            'company location': company_location,
            'url': url,
            'skills': cskills
        }
        info_naukri.append(data)

    driver.quit()

    return info_naukri



