import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



def scrape_foundit(text1):
    url = f'https://www.foundit.in/srp/results?query={text1}&locations=india'

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
    jobs = bs.find_all('div', class_='srpResultCardContainer')

    info = []

    for job in jobs:
        # TITLE = job.header.h2.a
        title = job.find('div', class_='jobTitle').text.strip()
        # link = TITLE.find('a').attrs['data-jk']

        company_name = job.find('div', class_='companyName').p.text.strip()
        # location_element = job.find('i', class_='material-icons', text='location_on').find_next('span', title=True)
        location = job.find('div', class_='details').text.strip()
        cskills = job.find('div', class_='skillDetails').text.strip()
        data = {
            'title': title,
            'company name': company_name,
            'company location': location,
            'url': url,
            'skills': cskills
        }
        info.append(data)

    driver.quit()
    return info

