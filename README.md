# Reddit Crypto Exchange

Fantasy Crypto Trading. Put your money where your mouth is!

Live realtime exchange prices.

Majority of coins supported from bitcoin to shitcoin.

### Usage

Commands: !JOIN, !CHECK [username], !SELL, !BUY

Sell and buy have the same format for transactions, like

```
!SELL 5 XMR
```

All sell and buy transactions use BTC as the other currency.


!CHECK on it's own will return your assets, but it can also be run with an username as an argument to check someone elses results.

### Running

Edit main.py with your Reddit API keys and password.

```
$ mongod
$ python3 main.py
```

### Dependencies

* Python3
* pymongo
* MongoDB server


#### Todo

* Web UI where you can see leaderboards and search for people.
* Clean up the code. It's horrible.
