# scrape_site1.py
import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def scrape_site1(text1):
    base_url = "https://in.indeed.com/"
    url = base_url + f"jobs?q={text1}&l=&from=searchOnHP&vjk=5d8a5ec3c615e23b"

    opts = Options()

    driver = webdriver.Chrome(options=opts)
    driver.get(url)

    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    bs = BeautifulSoup(response.text, "html.parser")

    # Use Selenium to scroll down and load more job listings
    scroll_count = 3  # Adjust the number of times to scroll
    for _ in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(5)

    bs = BeautifulSoup(driver.page_source, "html.parser")

    job_list = bs.find('ul', {'class': 'css-zu9cdh eu4oa1w0'})
    jobs = job_list.find_all('div', {'class': 'job_seen_beacon'})

    info_site1 = []
    for job in jobs:
        TITLE = job.find('h2', {'class': 'jobTitle'})
        title = TITLE.text
        link = TITLE.find('a').attrs['data-jk']
        url = f'https://in.indeed.com/viewjob?jk={link}&tk=1hcmgdnv4jrj2800&from=serp&vjs=3'
        company_name = job.find("span", {"class": "css-1x7z1ps eu4oa1w0"}).text
        company_location = job.find("div", {"class": "css-t4u72d eu4oa1w0"}).text
        cskills = job.find("div", {"class": "job-snippet"}).text.strip()
        data = {
            'title': title,
            'company name': company_name,
            'company location': company_location,
            'url': url,
            'skills': cskills
        }
        info_site1.append(data)

    driver.quit()

    return info_site1
