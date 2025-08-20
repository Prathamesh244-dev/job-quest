import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



def scrape_tj(text1):
    url = f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={text1}&txtLocation='

    opts = Options()
    opts.add_argument('--headless')  # Add this line to run Chrome in headless mode
    opts.add_argument('--disable-gpu')  # Add this line to disable GPU acceleration (often needed in headless mode)
    opts.add_argument('--window-size=1920x1080')  # Set your desired window size

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
    jobs = bs.find_all('li', class_='clearfix job-bx wht-shd-bx')

    info = []

    for job in jobs:
        TITLE = job.header.h2.a
        title = TITLE.text.strip()
        # link = TITLE.find('a').attrs['data-jk']
        url = job.header.h2.a['href']
        company_name = job.find('h3', class_='joblist-comp-name').text.strip()
        location_element = job.find('i', class_='material-icons', text='location_on').find_next('span', title=True)
        location = location_element['title']
        cskills = job.find('span', class_='srp-skills').text.strip()
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





