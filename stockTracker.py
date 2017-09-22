from colorama import Fore, Back, Style
import time
import json
from simplejson import JSONDecodeError
import requests
from requests.exceptions import ConnectionError
from urllib.error import HTTPError

print("Stock Tracker by Ivan Harmat")
print("To cancel press CTRL + C")

lastRefreshedGlobal = ""

def getJSON(url) :
    try :
        r = requests.get(url=url)
        jsonObj = r.json()
    except ConnectionError as e :
        return None
    return jsonObj

def getLastRefreshed(jsonObj) :
    lastRefreshed = jsonObj["Meta Data"]["3. Last Refreshed"]
    return lastRefreshed

def getLatestStockValue(jsonObj, timeStr) :
    stockValue = jsonObj["Time Series (1min)"][timeStr]
    return stockValue

def countdown(t):
    try :
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            if t <= 5 :
            	print(Fore.RED + " NEXT LOOKUP IN " + timeformat, end="\r")
            else :
            	print(" NEXT LOOKUP IN " + timeformat, end="\r")
            time.sleep(1)
            t -= 1
        print("                        ", end="\r")
        print(Style.RESET_ALL, end="\r")
        lookupStock()
    except KeyboardInterrupt :
        print(Style.RESET_ALL)
        print("------------------------------")
        print("Good Bye!")

def lookupStock() :
    global lastRefreshedGlobal
    jsonObj = getJSON("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=1min&apikey=G49UJ1RC50E64U3R")
    lastRefreshed = getLastRefreshed(jsonObj)
    if lastRefreshed != lastRefreshedGlobal :
        lastRefreshedGlobal = lastRefreshed
        stockValueJson = getLatestStockValue(jsonObj, lastRefreshed)
        print("Latest Stock Value - "+ lastRefreshed + " - "+ Fore.RED  +stockValueJson["1. open"] +" / "+ Fore.BLUE +stockValueJson["4. close"])   
        print(Style.RESET_ALL, end="\r")
    countdown(60) 

lookupStock()







