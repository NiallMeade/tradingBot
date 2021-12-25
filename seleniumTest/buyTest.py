from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

driver = webdriver.Firefox(executable_path=r'/home/niall/Downloads/geckodriver')

username = "niallbm101@gmail.com"
password = "@Munster101"

driver.get("https://www.trading212.com/en/login")

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'submit-button_input__3s_QD')))

driver.find_element_by_name("email").send_keys(username)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_class_name("submit-button_input__3s_QD").click()

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'portfolio-tab')))
time.sleep(3)

def buyStock(ticker, value) :
    driver.find_element_by_class_name("search-tab").click()
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'search-input')))
    driver.find_element_by_xpath("//input[@placeholder=\"Search all instruments\"]").send_keys("AA")
    time.sleep(3)
    searchResults = driver.find_elements_by_class_name("secondary-name")

    returnedTickers = []

    indexTracker = -1

    for t in searchResults:
        stringLen = len(t.text)
        returnedTickers.append(t.text[1:stringLen-1])
    print(returnedTickers)

    for t in returnedTickers :

        indexTracker += 1

        if t == ticker :
            driver.find_elements_by_class_name("secondary-name")[indexTracker].click()
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'trading-button')))
            time.sleep(3)
            driver.find_elements_by_class_name("trading-button")[1].click()
            time.sleep(1)
            driver.find_element_by_class_name("dropdown-header").click()
            time.sleep(1)
            driver.find_elements_by_class_name("dropdown-item-invest-by-type")[0].click()
            time.sleep(1)
            driver.find_element_by_class_name("css-jjd680").send_keys(value)
            time.sleep(1)
            driver.find_elements_by_class_name("accent-button")[1].click()
            time.sleep(1)
            driver.find_elements_by_class_name("accent-button")[1].click()
            time.sleep(1)
            driver.get("https://live.trading212.com/")

buyStock("AAPL", 1)
