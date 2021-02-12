import datetime
import yfinance as yf
import datetime as dt 
import pandas as pd 
import numpy as np

now = datetime.datetime.now().strftime("%Y-%m-%d")
data = yf.Ticker("1928.HK")
data = data.history(start="2010-01-01",  end=now)

data2= yf.download(tickers="1928.HK", period='1mo', interval='5m')
data2["textdt"]=data2.index.strftime("%d-%H:%M")
data2.set_index("textdt")["Close"].plot()

print(data2)

#data2["MA50"]=data2["Close"].rolling(window=50).mean()
#data2["MA20"]=data2["Close"].rolling(window=20).mean()

minhist=50
MAshort=10
MAlong=30
histdepth=100
histo=pd.DataFrame(columns=list(data2.columns)+["MAshort","MAlong","PNL"])
pnl=0
pos=0

for i in range(-histdepth-minhist,0): #browse in history of stock prices
    row= data2.iloc[i]
    #print(row)
    histo = histo.append(row)  # add new data to historics 
    price = row["Close"]
    if i>-histdepth:      # we have enough history to start the strategy
        MAS = histo.iloc[-MAshort:]["Close"].mean()
        MAL = histo.iloc[-MAlong:]["Close"].mean()
        #for the records 
        histo["MAshort"].iloc[-1]=MAS
        histo["MAlong"].iloc[-1]= MAL
        #print(histo["MA50"].iloc[-1],"moyenne ", histo.iloc[-50:]["Close"].mean())
        if (MAS>MAL) and pos==0:
            pos+=1
            buyprice=price
            print("buying at %f"% price)
            # since pos == 0 there is no PNL associated
        elif (MAS<MAL) and pos==1:
            pos+=-1
            sellprice=price
            pnl+= sellprice-buyprice
            print("selling at %f, pnl= %f"% (price,pnl))
        histo["PNL"].iloc[-1]=pnl
        #print(histo.iloc[-1]["MA50"],histo.iloc[-1]["MA20"],histo.iloc[-1]["PNL"])

histo.set_index("textdt")[["Close","MAshort","MAlong"]].plot()
histo.set_index("textdt")[["PNL"]].plot()