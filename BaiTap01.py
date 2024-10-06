from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

# Webdriver
driver = webdriver.Chrome()

try:
    # Open webpage
    url = 'https://en.wikipedia.org/wiki/Lists_of_musicians'
    driver.get(url)

    # Wait for 1 second
    time.sleep(1)

    # Get all ul tags
    ul_tags = driver.find_elements(By.TAG_NAME, 'ul')

    # Start with 'A'
    ul_musicians = ul_tags[21]

    # Get all <li> tags in ul_painters
    li_tags = ul_musicians.find_elements(By.TAG_NAME, 'li')

    # Create links
    links = []
    for tag in li_tags:
        try:
            link = tag.find_element(By.TAG_NAME, 'a').get_attribute('href')
            links.append(link)
        except:
            continue

    # Truy cập đến link đầu tiên trong phần "A"
    driver.get(links[0])

    # Get all ul tags
    ul_tags = driver.find_elements(By.TAG_NAME, 'ul')

    li_tags = ul_tags[24].find_elements(By.TAG_NAME, 'li')

    # Create links
    links = []
    for tag in li_tags:
        try:
            link = tag.find_element(By.TAG_NAME, 'a').get_attribute('href')
            links.append(link)
        except:
            continue

    musicians_dict = {'name': [], 'years_active': []}

    for link in links:
        driver.get(link)

        # Get name_of_the_band
        try:
            name = driver.find_element(By.TAG_NAME, 'h1').text
        except:
            name = ''

        years_active = ''
        # Get years_active
        try:
            years_active_element = driver.find_element(By.XPATH, "//tr[contains(., 'Years active')]")
            years_active = years_active_element.text
            years_active = ', '.join(re.findall(r'\d{4}–(?:\d{4}|present)', years_active))
        except:
            pass

        # Add to dict of painters
        musicians_dict['name'].append(name)
        musicians_dict['years_active'].append(years_active)

    df = pd.DataFrame(musicians_dict)
    print(df)

    file = 'musicians.xlsx'
    df.to_excel(file)

except:
    pass

driver.quit()
