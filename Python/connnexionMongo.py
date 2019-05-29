import pymongo

client = pymongo.MongoClient("mongodb+srv://bayo:rien@cluster0-gn4j1.mongodb.net/test?retryWrites=true")
collection = client.projet
tweets = collection.tweets
events = collection.events
fluxRSS = collection.fluxRSS