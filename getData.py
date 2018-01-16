#!/usr/bin/python3
# Copyright 2018 Ali Raheem

from json import loads
from urllib.request import urlopen
import db

class poloApi:
    """Class to pull ticker data from Poloniex.com"""
    url = "https://poloniex.com/public?command=returnTicker"
    def __init__(self, db):
        self.db = db
    def updatePrices(self):
        try:
            data = urlopen(self.url).read()
            data = loads(data)
            for datum in data.items():
                self.db.replace_one({'pair': datum[0]}, {"pair": datum[0], "last": datum[1]['last']}, upsert=True)
        except:
            print("Failed to update price")
    def getPrice(self, currency):
        try:
            return float(self.db.find_one({'pair': "BTC_"+currency})['last'])
        except:
            return -1

if ("__main__" == __name__):
    db = db.db()
    prices = db.db.prices
    api = poloApi(prices)
    api.updatePrices()
    print(api.getPrice('XMR'))

