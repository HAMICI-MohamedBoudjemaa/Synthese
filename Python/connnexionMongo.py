import pymongo
from pymongo import MongoClient

local = MongoClient('127.0.0.1', 27017)
db = local.WebSensors
tweets = db.tweets
events = db.events


"""client = pymongo.MongoClient("mongodb+srv://bayo:rien@cluster0-gn4j1.mongodb.net/test?retryWrites=true")
collection = client.projet
tweets = collection.tweet
events = collection.events"""
