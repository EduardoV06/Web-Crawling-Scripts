import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import time


search_term = str(input())

driver = webdriver.Safari()
driver.get(base_url)
driver.implicitly_wait(5)

search_bar = driver.find_element_by_id("cb1-edit")
search_bar.send_keys(search_term)
search_bar.submit()
base_url = driver.current_url

columns = ['Title', 'Price', 'Percetagen', 'Rating', 'Number of Reviews', 'Description']
results1 = []
while True:   
    
    driver.get(base_url)
    driver.implicitly_wait(5)

    elems = driver.find_elements_by_xpath("//a[@href]")
    list1 = [str(elem.get_attribute("href")) for elem in elems]
    links = list(filter(lambda v: re.match('.*/p/', v), list1))

    for link in links:
        driver.get(link)
        title = driver.find_element(By.CLASS_NAME, "ui-pdp-title").text
        price = driver.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text

        percetagen = 'NaN'
        try:
            percetagen = driver.find_element(By.CLASS_NAME, "andes-money-amount__discount").text
        except NoSuchElementException or TimeoutException:
            pass

        try:
            rating = driver.find_element(By.CSS_SELECTOR, "p.ui-review-capability__rating__average.ui-review-capability__rating__average--desktop").text
        except NoSuchElementException or TimeoutException:
            pass
        try:
            rating_num = driver.find_element(By.CSS_SELECTOR, "p.ui-review-capability__rating__label").text
        except NoSuchElementException or TimeoutException:
            pass

        description = driver.find_element(By.CLASS_NAME, "ui-pdp-description__content").text         
    
        results1.append((title, price, percetagen, rating, rating_num,description))
    
    driver.get(base_url)
    time.sleep(7)
    try:
        button = driver.find_element(By.LINK_TEXT, "Seguinte")
    except NoSuchElementException:
        break
    button.click()
    print('Page turned')
    current_url = driver.current_url
    base_url = current_url    


df = pd.DataFrame(results1, columns=columns)
df.drop_duplicates().reset_index()
df.to_csv(filepath, index=False)
driver.quit()
