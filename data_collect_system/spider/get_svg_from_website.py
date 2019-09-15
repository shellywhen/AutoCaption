from bs4 import BeautifulSoup
from selenium import webdriver
import codecs
import time

def get_svg(filename, driver):
    print(filename)
    driver.find_element_by_id("change_button").click()
    driver.implicitly_wait(0.1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # print(str(soup.select("svg")[0]))
    with codecs.open(filename, "wb", 'utf-8') as f:
        f.write(str(soup.select("svg")[0]))

def get_many_svg(url,number):

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    print(url)
    inputElement = driver.find_element_by_id("name")
    inputElement.send_keys('spider_rule_ocq')
    inputElement.send_keys(Keys.ENTER)
    time.sleep(3)
    for i in range(number):
        driver.find_element_by_id('submit').click()
        time.sleep(0.2)
        # get_svg(file_name, driver)
    driver.quit()

get_many_svg("localhost:8000",100)
