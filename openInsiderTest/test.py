from os import sep
import time as t
from numpy.core.numeric import roll
import pandas as pd
import numpy as np
from pandas.core.indexes.api import all_indexes_same
#from yahoo_fin import stock_info
import yfinance as yf
import csv
import datetime
import numpy as np

from yahoo_fin.stock_info import get_data


file_ = pd.read_csv("openinsiderAugust.csv", sep = ',')
A = np.array(file_[["FilingDate", "Ticker"]])
FilingDateEdit = str
BuyPrices = []
SellPrices = []

print(A)

for i in A:
    Date = i[0]
    FilingDateEdit = Date[6:10] + "-" + Date[3:5] + "-" + Date[:2]
    print(FilingDateEdit)
    FilingDateDT = datetime.date(int(Date[6:10]), int(Date[3:5]), int(Date[:2]))
    ScanFinishDT = np.busday_offset(FilingDateDT, 4, roll="forward")
    print(FilingDateDT)
    print(ScanFinishDT)
    TimeInt = int(Date[11:13])

    DateInt = int(Date[:2])
    HourInt = int(Date[11:13])
    MinuteInt = int(Date[14:16])
    HourIntAdjusted = HourInt/24
    MinuteIntAdjusted = MinuteInt/1440
    FilingTimeInt = DateInt + HourIntAdjusted + MinuteIntAdjusted

    SellTimeDT = np.busday_offset(FilingDateDT, 2, roll="forward")
    print(SellTimeDT)
    SellDateInt = str(SellTimeDT)[8:]
    SellTimeInt = int(SellDateInt) + HourIntAdjusted + MinuteIntAdjusted

    if TimeInt<16 and TimeInt > 9:
        print(str(TimeInt))
        data = []
        data = yf.download(tickers=i[1], start=FilingDateEdit, end=str(ScanFinishDT), interval="5m")

        if len(data) > 1 :
            print("Data Array Lenght")
            print(len(data))
            print("got here 1")
            data.to_csv( i[1] + ".csv")
            # data = stock_info.get_data(i[1], start_date= FilingDateEdit, end_date= str(ScanFinishDT), interval= "1m")
            print(data)

            csvFile = pd.read_csv(i[1] + ".csv", sep = ",")
            StructuredData = np.array(csvFile[["Datetime","Open"]])
            print(StructuredData)

            TimeStamps = []
            StructuredOpenData = []

            for row in StructuredData:
                DateRow = row[0]
                DateStamp = int(DateRow[8:10])
                HourStamp = int(DateRow[11:13])
                MinuteStamp = int(DateRow[14:16])
                HourStampAdjusted = HourStamp/24
                MinuteStampAdjusted = MinuteStamp/1440

                DecTime = DateStamp + HourStampAdjusted + MinuteStampAdjusted
                TimeStamps.append(DecTime)

                OpenRow = row[1]
                Open = float(OpenRow)
                StructuredOpenData.append(Open)
            
            TimeStampedData = []
            TimeStampedData = np.hstack((StructuredData, np.atleast_2d(TimeStamps).T))
            print(TimeStampedData)

            #StructuredOpenData = StructuredData[1:]
            print(TimeStamps)
            print("got here 2")
            print(FilingTimeInt)
            BuyIndex = min(range(len(TimeStamps)), key=lambda i: abs(TimeStamps[i]-FilingTimeInt))
            SellIndex = min(range(len(TimeStamps)), key=lambda i: abs(TimeStamps[i]-SellTimeInt))
            print(BuyIndex)

            print(StructuredOpenData)
            print("list of open prices")
            print(StructuredOpenData[BuyIndex])
            BuyPrices.append(StructuredOpenData[BuyIndex])
            SellPrices.append(StructuredOpenData[SellIndex])

            #StructuredDataOpen = StructuredData[1]
            #print(StructuredDataOpen[:index])
            #index = (np.abs(TimeStamps - FilingTimeInt)).argmin()

            #difference_array = np.absolute(int(StructuredData[1:]) - FilingTimeInt)
    
    else:
        print("outside hours")


    t.sleep(1)

# PricesDict = {"BuyPrices", "SellPrices"}
# Prices = pd.DataFrame(PricesDict)
# Prices.to_csv("000FINAL.csv", index=False)

Prices = np.column_stack([BuyPrices, SellPrices])
PricesPD = pd.DataFrame(Prices)
PricesPD.to_csv("000FINAL.csv", index=False)

print("All Done")
