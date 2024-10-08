from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

import sqlite3

######################################################
# 0. Tạo cơ sở dữ liệu
conn = sqlite3.connect('musicians.db')
c = conn.cursor()
try:
    c.execute('''
        CREATE TABLE musician (
            id integer primary key autoincrement,
            name text,
            years_active text
        )
    ''')
except Exception as e:
    print(e)


def them(name, years_active):
    conn = sqlite3.connect('musicians.db')
    c = conn.cursor()
    # Them vao co so du lieu
    c.execute('''
        INSERT INTO musician(name, years_active)
        VALUES (:name, :years_active)
    ''',
      {
          'name': name,
          'years_active': years_active
      })
    conn.commit()
    conn.close()


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
        except Exception as e:
            print(e)
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
        except Exception as e:
            print(e)
            continue

    musicians_dict = {'name': [], 'years_active': []}

    for link in links:
        driver.get(link)

        # Get name_of_the_band
        try:
            name = driver.find_element(By.TAG_NAME, 'h1').text
        except Exception as e:
            print(e)
            name = ''

        years_active = ''
        # Get years_active
        try:
            years_active_element = driver.find_element(By.XPATH, "//tr[contains(., 'Years active')]")
            years_active = years_active_element.text
            years_active = ', '.join(re.findall(r'\d{4}–(?:\d{4}|present)', years_active))
        except Exception as e:
            print(e)

        them(name, years_active)

        # Add to dict of painters
        musicians_dict['name'].append(name)
        musicians_dict['years_active'].append(years_active)

    df = pd.DataFrame(musicians_dict)
    print(df)

    # file = 'musicians.xlsx'
    # df.to_excel(file)

except Exception as e:
    print(e)

driver.quit()
