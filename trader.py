#!/usr/bin/python3

import db

class trader:
    """Manage Traders allow them to buy and sell"""
    def __init__(self, name, db):
        self.name = name
        self.db = db
        self.getAssets()
    def getAssets(self):
        try:
            self.assets = self.db.find_one({"name": self.name})['assets']
        except:
            self.rebuy()
        return self.assets
    def setAssets(self):
        self.db.update_one({"name": self.name},{'$set': {"assets": self.assets}}, upsert=True)
    def rebuy(self):
        self.assets = {'BTC': 1}
        self.db.update_one({"name": self.name},{'$set': {"assets": self.assets}}, upsert=True)
    def sell(self, currency, amount, price):
        amount = round(amount, 8)
        try:
            if(self.assets[currency] <=  amount):
                amount = self.assets[currency]
            self.assets[currency] -= amount
            self.assets['BTC'] += price * amount
            self.assets['BTC'] = round(self.assets['BTC'], 8)
            self.setAssets()
        except Exception as e:
            print(e)
            return -1
    def buy(self, currency, amount, price):
        amount = round(amount, 8)
        try:
            if(self.assets['BTC'] >= amount * price):
                self.assets['BTC'] -= amount * price
                self.assets['BTC'] = round(self.assets['BTC'], 8)
                self.assets[currency] += amount
                self.assets[currency] = round(self.assets[currency], 8)
                self.setAssets()
            else:
                print("Insufficient funds")
                return -1
        except Exception as e:
            print(e)
            return -1

if ("__main__" == __name__):
    db = db.db()
    traders_db = db.db.traders_db
    me = trader("Ali", traders_db)
    print(me.assets)
    import getData
    api = getData.poloApi(db.db.prices)
    price = api.getPrice('XMR')
    if(price == -1):
        print("Error not found")
    me.buy('VTC', 100000, api.getPrice('VTC'))
    me.sell('VTC', 100000, api.getPrice('VTC'))
    me.buy('VTC', 10, api.getPrice('VTC'))
    me.buy('XMR', 0.5, price)
    me.sell('XMR', 10, price)
    print(me.assets)
