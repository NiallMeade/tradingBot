import requests #<--- to get webpages in their html form
from bs4 import BeautifulSoup #<-- to parse html and find specific elements
import csv
from datetime import datetime, timedelta
from math import isnan
import numpy as np
import time
import pandas as pd
from yahoo_fin import stock_info
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

driver = webdriver.Firefox(executable_path=r'/home/niall/Downloads/geckodriver')

username = ""
password = ""

driver.get("https://www.trading212.com/en/login")

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'submit-button_input__3s_QD')))

driver.find_element_by_name("email").send_keys(username)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_class_name("submit-button_input__3s_QD").click()

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'portfolio-tab')))
time.sleep(3)

url = "http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=730&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1" #change this string for different results

#this code gets tickers and dates for the url
requestvalue = requests.get(url)
soup = BeautifulSoup(requestvalue.content, "html.parser")

data = []

for i in soup.find("table", class_="tinytable").find("tbody").find_all("tr"):
    date = i.find("a").get_text()
    ticker = i.find("b").find("a").get_text()

    data.append(ticker)

topTicker = data[0]
print(topTicker)

topTickers = []

for ticker in data[:5]:
    topTickers.append(ticker)

print("-------")
print(topTickers)
print("-------")

def sellStock(ticker, value) :
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
            driver.find_elements_by_class_name("trading-button")[0].click()
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

def buyStock(ticker, value) :
    print("here")
    driver.find_element_by_class_name("search-tab").click()
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'search-input')))
    driver.find_element_by_xpath("//input[@placeholder=\"Search all instruments\"]").send_keys(ticker)
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

def buyValue():

    driver.find_element_by_class_name("portfolio-tab").click()
    driver.find_element_by_class_name("account-status-header-label").click()
    funds = driver.find_elements_by_class_name("formatted-price-part")

    print(len(funds))
    fundsText = []

    for f in funds:
        fundsText.append(f.text)

    listLen = len(fundsText)

    freeFundsStr = "".join(fundsText[4:6])
    freeFundsStr = "".join(fundsText[listLen-5:listLen-3])
    portfolioFundsStr = "".join(fundsText[7:9])
    portfolioFundsStr = "".join(fundsText[listLen-2:listLen])
    totalFundsStr = "".join(fundsText[listLen-8:listLen-6])
    
    freeFunds = float(freeFundsStr)
    portfolioFunds = float(portfolioFundsStr)
    totalFunds = float(totalFundsStr)
    fundsRatio = freeFunds/totalFunds

    if totalFunds == freeFunds:
        value = freeFunds/3
        return value
    elif fundsRatio > 0.56 :
        value = freeFunds/2
        return value
    elif freeFunds > 1.5:
        value = freeFunds
        return value
    else:
        value = 0
        return value

while True:

    try:

        time.sleep(300)

        hour = datetime.now().hour
        min = datetime.now().minute
        hourTS = hour + min/60

        requestvalue = requests.get(url)
        soup = BeautifulSoup(requestvalue.content, "html.parser")

        liveTrades = pd.read_csv("liveTrades.csv")

        tickerData = []

        indexTracker = -1

        tradeHistory = pd.read_csv("tradeHistory.csv")

        # print(stock_info.get_live_price(tradeHistory.at[2, "ticker"]))

        for i in soup.find("table", class_="tinytable").find("tbody").find_all("tr"):
            date = i.find("a").get_text()
            ticker = i.find("b").find("a").get_text()
            tickerData.append(ticker)

        for t in liveTrades["closeTime"]:
            indexTracker += 1
            if t < datetime.timestamp(datetime.now()):

                try:

                    print("sell this" + "(" + liveTrades.at[indexTracker, "ticker"] + ")")
                    liveTrades = liveTrades.drop(labels=indexTracker, axis=0)

                    sellStock(t, 999999999)
                
                except:
                    print("PROBLEM SELLING - " + t)

        liveTrades.to_csv('liveTrades.csv', mode='w', index=False)

        indexTracker = -1

        for t in tradeHistory["closeTime"]:
            indexTracker += 1
            if t < datetime.timestamp(datetime.now()):
                tradeHistory.at[indexTracker, "sellPrice"] = stock_info.get_live_price(tradeHistory.at[indexTracker, "ticker"])

        tradeHistory.to_csv('tradeHistory.csv', mode='w', index=False)


        if tickerData[0:5] == topTickers:
            print("same ticker, do nothing")
            print(datetime.now())
            print(tickerData[0:5])

        elif tickerData[0:5] != topTickers:
            print("----------")
            print("new trade")
            print("----------")
            newTrades = np.setdiff1d(tickerData[0:5], topTickers)
            print(newTrades)

            topTickers = tickerData[0:5]

            if hourTS > 14.5 and hourTS < 21:

                for t in newTrades:

                    try:

                        buyAmount = buyValue()

                        if buyAmount > 0 :
                            buyStock(t, buyAmount)

                            sellDatetime = datetime.now() + pd.tseries.offsets.BusinessDay(n = 1)
                            buyTimestamp = datetime.timestamp(datetime.now())
                            sellTimestamp = datetime.timestamp(sellDatetime)

                            new_row = [t, "open", buyTimestamp, sellTimestamp]
                            tickerDF = pd.DataFrame([new_row], columns=["ticker", "positionState", "openTime", "closeTime"])
                            tickerDF.to_csv('liveTrades.csv', mode='a', header=False, index=False)

                            history_row = [t, buyTimestamp, sellTimestamp, datetime.now(), stock_info.get_live_price(t), 0]
                            historyDF = pd.DataFrame([history_row], columns=["ticker", "openTime", "closeTime", "openDate", "openPrice", "sellPrice"])
                            historyDF.to_csv('tradeHistory.csv', mode='a', header=False, index=False)
                        
                        else:
                            print("insufficent funds")
                    
                    except:
                        print("PROBLEM WHILE BUYING - " + Exception)
            
            else:
                print("outside hours")

        else:
            print("something unexpected happened")

        print(datetime.now())

    except:

        print(Exception)
