#!/usr/bin/python3

from pymongo import MongoClient

class db:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.exchange_bot
