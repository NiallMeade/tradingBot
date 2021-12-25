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
from forex_python.converter import CurrencyRates
import math

driver = webdriver.Firefox(executable_path=r'/home/niall/Downloads/geckodriver')

username = ""
password = ""

# driver.get("https://trader.degiro.nl/login/ie?_ga=2.256698568.2124293258.1631614785-1743120408.1631614785#/login")

# WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "_1EEaqLAc")))

# driver.find_element_by_name("username").send_keys(username)
# driver.find_element_by_name("password").send_keys(password)
# driver.find_element_by_class_name("_1EEaqLAc").click()

# WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "_1s3g8KO2")))
# time.sleep(3)

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

def login():
    driver.get("https://trader.degiro.nl/login/ie?_ga=2.256698568.2124293258.1631614785-1743120408.1631614785#/login")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "_1EEaqLAc")))

    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_class_name("_1EEaqLAc").click()

    time.sleep(3)

def sell(ticker):

    login()
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
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "_2TZn-T5Q")))
                driver.find_elements_by_class_name("_2TZn-T5Q")[1].click()
                quantity = driver.find_element_by_css_selector('[data-field="size"]').get_attribute("title")
                print(quantity)
                sellPrice = driver.find_elements_by_class_name("_1h_eTEhu ")[1].text
                sellPrice = float(sellPrice) - 0.01
                print(sellPrice)
                driver.find_elements_by_class_name("_3jh6ix0v")[1].send_keys(str(sellPrice))
                driver.find_elements_by_class_name("_3jh6ix0v")[2].send_keys(quantity)
                driver.find_elements_by_class_name("duvfw-AB")[1].click()
                time.sleep(3)
                driver.find_elements_by_class_name("duvfw-AB")[1].click()
                break
            else:
                print("ticker not the same")

def buy(ticker, quantity):

    login()
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

def buyDecision(ticker) :

    login()
    time.sleep(2)
    driver.find_element_by_class_name("_2XHpHYyN").click()

    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "_8Dp1KM5D")))
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
        allocatedFunds = availableFunds * 0.98
        noShares = allocatedFunds/stockPrice
        noShares = math.floor(noShares)

        if noShares > 0 and allocatedFunds > 100:
            return noShares

        else:
            return noShares

    else:
        return 0

while True:

    try:

        time.sleep(30)

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
                    sell(liveTrades.at[indexTracker, "ticker"])
                    liveTrades = liveTrades.drop(labels=indexTracker, axis=0)
                
                except Exception as e:
                    print("PROBLEM SELLING - " + t)
                    print(e)

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

            if hourTS > 14.5 and hourTS < 20:

                for t in newTrades:

                    try:
                        print(t)
                        print(type(t))
                        t = str(t)
                        print(t)
                        print(type(t))

                        buyAmount = buyDecision(str(t))
                        print("buy amount " + buyAmount)

                        if buyAmount > 0 :
                            buy(str(t), buyAmount)

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
                    
                    except Exception as e:
                        print("PROBLEM WHILE BUYING - " + e)
            
            else:
                print("outside hours")

        else:
            print("something unexpected happened")

        print(datetime.now())

    except Exception as e:
        print(e)
