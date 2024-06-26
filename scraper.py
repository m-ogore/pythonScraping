from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
# from selenium.webdriver.common.keys import Keys

def scraper():

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

    page_source = my_driver.page_source
    my_driver.close()

    my_soup = BeautifulSoup(page_source, 'html.parser')

    my_table = my_soup.find('table', {'class': 'table table-striped sortable'})

    my_headers = [header.text for header in my_table.find('tr').find_all('th')]

    my_headers.extend(['',''])

    my_df = pd.DataFrame(columns=my_headers if my_headers else None)

    my_data = []
    
    for row in my_table.find('tbody').find_all('tr'):
        cells = row.find_all('td')

        ROW = [cell.text.strip() for cell in cells]

        my_data.append(ROW)

    print("Data:", len(my_data[0]))
    print(my_data[0])
    print("headers:", len(my_headers))

    my_df = pd.DataFrame(my_data, columns=my_headers if my_headers else None)
    my_df.to_csv('aluswe.csv', index=False)


    return my_df
