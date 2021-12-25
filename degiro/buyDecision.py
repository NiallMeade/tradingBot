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

username = "NiallMeade"
password = "@Munster101"

driver.get("https://trader.degiro.nl/login/ie?_ga=2.256698568.2124293258.1631614785-1743120408.1631614785#/login")

WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "_1EEaqLAc")))

driver.find_element_by_name("username").send_keys(username)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_class_name("_1EEaqLAc").click()

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "_1s3g8KO2")))
time.sleep(3)

def buyDecision(ticker) :
    driver.find_element_by_class_name("_2XHpHYyN").click()
    time.sleep(2)
    funds = driver.find_elements_by_class_name("_8Dp1KM5D")
    fundsText = []
    exchR = CurrencyRates().get_rate("EUR","USD")
    print(exchR)

    for f in funds:
        fundsText.append(f.text)
    
    print(fundsText)

    balance = fundsText[0]
    balance = balance[2:]
    balance = float(balance)
    balance = balance * exchR

    availableFunds = fundsText[2]
    availableFunds = availableFunds[2:]
    availableFunds = float(availableFunds)
    availableFunds = availableFunds * exchR

    fundsRatio = availableFunds/balance

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
    
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "_1-App5Fj")))
    driver.find_elements_by_class_name("_1-App5Fj")[1].click()
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "_3iCGaL0N")))
    driver.find_elements_by_class_name("_3iCGaL0N")[1].click()
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "_1h_eTEhu")))
    stockPrice = driver.find_elements_by_class_name("_1h_eTEhu")[0].get_attribute("title")
    stockPrice = float(stockPrice)
    stockPrice = stockPrice + 0.01
    print(stockPrice)

    if balance == availableFunds:
        allocatedFunds = availableFunds/3
        noShares = allocatedFunds/stockPrice
        roundUpShares = math.ceil(noShares)
        roundUpFunds = roundUpShares*stockPrice
        noShares = math.floor(noShares)


        if roundUpFunds/allocatedFunds < 1.15 and allocatedFunds > 100:
            return roundUpShares

        elif allocatedFunds > 100:
            return noShares

        else:
            return 0

    elif fundsRatio > 0.56 :
        allocatedFunds = availableFunds/2
        noShares = allocatedFunds/stockPrice
        roundUpShares = math.ceil(noShares)
        roundUpFunds = roundUpShares*stockPrice
        noShares = math.floor(noShares)

        if roundUpFunds/allocatedFunds < 1.075 and allocatedFunds > 100:
            return roundUpShares

        elif allocatedFunds > 100:
            return noShares
        
        else:
            return 0

    elif availableFunds > 1.5:
        allocatedFunds = availableFunds * 0.95
        noShares = allocatedFunds/stockPrice
        noShares = math.floor(noShares)

        if noShares > 0 and allocatedFunds > 100:
            return noShares

        else:
            return noShares

    else:
        return 0

buyDecision("AAPL")