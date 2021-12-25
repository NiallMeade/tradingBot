from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from forex_python.converter import CurrencyRates
import re
import math

driver = webdriver.Firefox(executable_path=r'/home/niall/Downloads/geckodriver')

username = ""
password = ""

driver.get("https://trader.degiro.nl/login/ie?_ga=2.256698568.2124293258.1631614785-1743120408.1631614785#/login")

WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "_1EEaqLAc")))

driver.find_element_by_name("username").send_keys(username)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_class_name("_1EEaqLAc").click()

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "_1s3g8KO2")))
time.sleep(3)

def buy(ticker, quantity):

    driver.find_element_by_class_name("duvfw-AB").click()
    time.sleep(1)
    driver.find_element_by_class_name("duvfw-AB").click()
    time.sleep(1)
    driver.find_element_by_class_name("_3ayi1oaj").send_keys(ticker)
    time.sleep(2)
    searchResult = driver.find_elements_by_class_name("_21l9ETAc")
    unformattedResultTickers = []

    for r in searchResult:
        unformattedResultTickers.append(r.text)

    print(unformattedResultTickers)

    indexTracker = -1

    for l in unformattedResultTickers:
            indexTracker += 1

            if ticker in l:
                driver.find_elements_by_class_name("_21l9ETAc")[indexTracker].click()
            else:
                print("ticker not the same")
    
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "_1h_eTEhu ")))
    limitPrice = driver.find_elements_by_class_name("_1h_eTEhu ")[0].get_attribute("title")
    limitPrice = float(limitPrice) - 1.01
    limitPrice = str(limitPrice)

    driver.find_elements_by_class_name("_3jh6ix0v")[1].send_keys(limitPrice)
    driver.find_elements_by_class_name("_3jh6ix0v")[2].send_keys(quantity)
    driver.find_elements_by_class_name("duvfw-AB")[1].click()
    time.sleep(3)
    driver.find_elements_by_class_name("duvfw-AB")[1].click()

buy("CFFN", 1)
