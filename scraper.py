from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_pages():

    PASSWORD = open('creds.txt', 'r').read()

    URL = 'https://intranet.aluswe.com/resource_links'

    brave_exe = '/usr/bin/brave-browser'

    my_options = webdriver.ChromeOptions()
    my_options.binary_location = brave_exe

    my_driver = webdriver.Chrome(options=my_options)
    my_driver.get(URL)

    email_field = my_driver.find_element(By.ID, 'user_email')
    password_field = my_driver.find_element(By.ID, 'user_password')
    login_btn = my_driver.find_element(By.NAME, 'commit')

    email_field.send_keys('wdebela@alueducation.com')
    password_field.send_keys(PASSWORD)
    login_btn.click()

    page_sources = []
    
    try:
        while True:
            # Assuming 'commit' is the name of the next button you want to click
            next_btn = WebDriverWait(my_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='universal-pagination']/a[contains(text(), 'Next')]")))
            
            # Append the current page source to the list
            page_sources.append(my_driver.page_source)
            
            # Click the next button
            next_btn.click()
            
            # Optionally, you can add a delay here if necessary
            WebDriverWait(my_driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        my_driver.quit()
    print(f"{'#'*5} Done getting page sources {'#'*5}")
    return page_sources
def scraper():

    my_data = []

    page_sources = get_pages()
    for page_source in page_sources:
        my_soup = BeautifulSoup(page_source, 'html.parser')

        my_table = my_soup.find('table', {'class': 'table table-striped sortable'})

        my_headers = [header.text for header in my_table.find('tr').find_all('th')]

        my_headers.extend(['',''])

        my_df = pd.DataFrame(columns=my_headers if my_headers else None)

    
    
        for row in my_table.find('tbody').find_all('tr'):
            cells = row.find_all('td')

            ROW = [cell.text.strip() for cell in cells]

            my_data.append(ROW)

    print("Data:", len(my_data[0]))
    print(my_data[0])
    print("headers:", len(my_headers))

    my_df = pd.DataFrame(my_data, columns=my_headers if my_headers else None)
    #my_df.to_csv('aluswe.csv', index=False)

    print(f"{'#'*5} Done putting in dataframe {'#'*5}")


    return my_df
