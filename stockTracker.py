from colorama import Fore, Back, Style
import sys
import time
import json
from simplejson import JSONDecodeError
import requests
from requests.exceptions import ConnectionError
from urllib.error import HTTPError

print("Stock Tracker by Ivan Harmat")
print("To cancel press CTRL + C")

stockSymbol = "AAPL"
if len(sys.argv) > 1 :
    stockSymbol = sys.argv[1]

lastRefreshedGlobal = ""

def getJSON(url) :
    try :
        r = requests.get(url=url)
        jsonObj = r.json()
    except ConnectionError as e :
        return None
    return jsonObj

def getLastRefreshed(jsonObj) :
    try :
        lastRefreshed = jsonObj["Meta Data"]["3. Last Refreshed"]
    except Exception :
        return None
    return lastRefreshed

def getLatestStockValue(jsonObj, timeStr) :
    try :
        stockValue = jsonObj["Time Series (1min)"][timeStr]
    except Exception :
        return None 
    return stockValue

def countdown(minutes):
    seconds = minutes * 60
    try :
        while seconds:
            mins, secs = divmod(seconds, 60)
            timeformat = '{:02d}:{:02d}'.format(minutes, secs)
            if seconds <= 5 :
            	print(Fore.RED + " NEXT LOOKUP IN " + timeformat, end="\r")
            else :
            	print(" NEXT LOOKUP IN " + timeformat, end="\r")
            time.sleep(1)
            seconds -= 1
            minutes = int(seconds / 60)
        print("                        ", end="\r")
        print(Style.RESET_ALL, end="\r")
        lookupStock()
    except KeyboardInterrupt :
        print(Style.RESET_ALL)
        print("------------------------------")
        print("Good Bye!")

def lookupStock() :
    global lastRefreshedGlobal
    jsonObj = getJSON("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+stockSymbol+"&interval=1min&apikey=G49UJ1RC50E64U3R")
    lastRefreshed = getLastRefreshed(jsonObj)
    if lastRefreshed != None :
        if lastRefreshed != lastRefreshedGlobal :
            lastRefreshedGlobal = lastRefreshed
            stockValueJson = getLatestStockValue(jsonObj, lastRefreshed)
            if stockValueJson != None :
                stockOpen = float(stockValueJson["1. open"])
                stockClose = float(stockValueJson["4. close"])
                percent = str(round((stockClose - stockOpen) / 100, 4))
                if stockOpen > stockClose :
                    print(stockSymbol + " - Latest Stock Value - "+ lastRefreshed + " - Open : "+ Fore.YELLOW  +str(stockOpen)+Style.RESET_ALL+", Close : "+Fore.CYAN+ str(stockClose)+Fore.RED+" ("+percent+"%)")  
                elif stockOpen == stockClose:
                    print(stockSymbol + " - Latest Stock Value - "+ lastRefreshed + " - Open : "+ Fore.YELLOW  +str(stockOpen)+Style.RESET_ALL+", Close : "+Fore.CYAN+ str(stockClose)+Fore.BLUE+" (0%)")
                else :
                    print(stockSymbol + " - Latest Stock Value - "+ lastRefreshed + " - Open : "+ Fore.YELLOW  +str(stockOpen)+Style.RESET_ALL+", Close : "+Fore.CYAN+ str(stockClose)+Fore.GREEN+" ("+percent+"%)")

            print(Style.RESET_ALL, end="\r")
        countdown(2)
    else :
        print("Wrong stock symbol - "+stockSymbol) 

lookupStock()







