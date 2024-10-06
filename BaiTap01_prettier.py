# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    # Open the Wikipedia page containing lists of musicians
    wiki_url = 'https://en.wikipedia.org/wiki/Lists_of_musicians'
    driver.get(wiki_url)

    # Pause for 1 second to allow the page to load
    time.sleep(1)

    # Find all unordered list (ul) elements on the page
    all_ul_tags = driver.find_elements(By.TAG_NAME, 'ul')

    # Select the ul element that contains musicians whose genre starts with "A"
    ul_musicians_genre_a = all_ul_tags[21]

    # Get all list item (li) elements within the selected ul element
    li_musicians_genre_a = ul_musicians_genre_a.find_elements(By.TAG_NAME, 'li')

    # Extract links to individual musician pages
    musician_links = []
    for li in li_musicians_genre_a:
        try:
            musician_link = li.find_element(By.TAG_NAME, 'a').get_attribute('href')
            musician_links.append(musician_link)
        except Exception as e:
            # Skip if there's any issue finding the link
            continue

    # Access the first musician's page under genre "A"
    driver.get(musician_links[0])

    # Extract all ul elements from the musician page
    musician_ul_tags = driver.find_elements(By.TAG_NAME, 'ul')

    # Select the relevant ul element containing musician details
    li_musicians_details = musician_ul_tags[24].find_elements(By.TAG_NAME, 'li')

    # Extract links to detailed pages about musicians
    musician_detail_links = []
    for li in li_musicians_details:
        try:
            detail_link = li.find_element(By.TAG_NAME, 'a').get_attribute('href')
            musician_detail_links.append(detail_link)
        except Exception as e:
            continue

    # Dictionary to store musician names and years active
    musicians_data = {'name': [], 'years_active': []}

    # Loop through the detailed links and extract musician data
    for detail_link in musician_detail_links:
        driver.get(detail_link)

        # Extract the name of the musician or band (found in the <h1> tag)
        try:
            musician_name = driver.find_element(By.TAG_NAME, 'h1').text
        except Exception as e:
            musician_name = ''

        # Initialize empty string for years active
        musician_years_active = ''

        # Extract the 'Years active' information if available
        try:
            years_active_element = driver.find_element(By.XPATH, "//tr[contains(., 'Years active')]")
            years_active_text = years_active_element.text
            musician_years_active = ', '.join(re.findall(r'\d{4}–(?:\d{4}|present)', years_active_text))
        except Exception as e:
            pass

        # Append extracted data to the dictionary
        musicians_data['name'].append(musician_name)
        musicians_data['years_active'].append(musician_years_active)

    # Create a pandas DataFrame from the musician data dictionary
    musicians_df = pd.DataFrame(musicians_data)
    print(musicians_df)

    # Save the DataFrame to an Excel file
    output_file = 'musicians.xlsx'
    musicians_df.to_excel(output_file)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver
    driver.quit()
