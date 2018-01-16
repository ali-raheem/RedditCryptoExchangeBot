#!/usr/bin/python3
# Copyright 2018 Ali Raheem
from db import db as database
from getData import poloApi
from trader import trader
import praw
from json import dumps
import time

def handle_cmd(comment):
    try:
        username = comment.author.name
        cmd = comment.body.replace("u/crypto-trader-bot", "").replace('/', '').strip().upper()
        t = trader(username, db.db.traders_db)
        if(cmd.startswith('!JOIN')):
            t = trader(comment.author.name, db.db.traders_db)
            print("{} wants to join the fun!".format(comment.author.name))
            comment.reply("You have been added! Use !CHECK to see your assets.")
            return
        elif(cmd.startswith('!CHECK')):
            try:
                username = cmd.split(' ')[1]
            except Exception as e:
                username = comment.author.name
            msg = checkBalance(username)
            comment.reply(msg)
            return
        else:
            action, amount, currency = cmd.split(' ')
            print("{} wants to {} {} {}.".format(username, action, amount, currency))
            action = action.upper()
            currency = currency.upper()
            if("!BUY" == action):
                p = api.getPrice(currency)
                if (-1 == p):
                    comment.reply("Error: You want to buy what?")
                    return
                if('!' == amount):
                    amount = float(t.assets['BTC'])/p
                else:    
                    amount = float(amount)
                r = t.buy(currency, amount, p)
                if (-1 == r):
                    comment.reply("Error: Insufficient funds.")
                else:
                    comment.reply("Success: Bought {} {} at {} BTC/{}".format(amount, currency, p, currency))            
            elif("!SELL" == action):
                p = api.getPrice(currency)
                if('!' == amount):
                    amount = float(t.assets[currency])-0.00000001
                else:    
                    amount = float(amount)
                if (-1 == p):
                    comment.reply("Error: You want to buy what? Only ")
                    return
                r = t.sell(currency, amount, p)
                if(-1 == r):
                    comment.reply("Error: Insufficient funds")
                else:
                    comment.reply("Success: Sold {} {} at {} BTC/{}".format(amount, currency, p, currency))            
    except Exception as e:
        print("Failed to handle cmd")
        print(e)

def checkBalance(username):
    t = trader(username, db.db.traders_db)
    value = 0
    msg = "Breakdown of assets for **{}**\n\n".format(username)
    for asset in t.assets.items():
        msg += "* {} {}\n\n".format(asset[0], asset[1])
        p = api.getPrice(asset[0])
        if(-1 == p):
            continue
        value +=p*asset[1]
    value += t.assets['BTC']
    value = round(value, 8)
    msg += "*Worth a total of {} BTC ".format(value)
    msg += time.strftime("on %a, %d %b %Y %H:%M:%S +0000*", time.gmtime())
    return msg

if ("__main__" == __name__):
    print("Starting game!")
    useragent = "linux-x64:cryptotraderbot:v0.1.1 (by /u/aliraheem)"
    db = database()
    api = poloApi(db.db.prices)
    lastUpdate = 0
    lastRedditScan = 0
    reddit = praw.Reddit(client_id = '',
                         client_secret = '',
                         user_agent = 'useragent,
                         username  = '',
                         password = '')
    while True:
        try:
            if(time.time() - lastRedditScan > 30):
                print("Scanning reddit...")
                lastRedditScan = time.time()
                for comment in reddit.inbox.stream():
                    if(comment.created_utc < lastRedditScan):
                        continue
                    if(time.time() - lastUpdate > 60):
                        print("Prices stale...")
                        api.updatePrices()
                        lastUpdate = time.time()
                        print("Updated.")
                    handle_cmd(comment)
                print("Done.")
        except Exception as e:
            print(e)
