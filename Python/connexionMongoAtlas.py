import pymongo

#client = pymongo.MongoClient("mongodb+srv://bayo:rien@cluster0-gn4j1.mongodb.net/test?retryWrites=true")
client = pymongo.MongoClient("mongodb+srv://m2b:dl4rz7*I@cluster1-das7g.mongodb.net/test")
collection = client.websensors
fluxRSS = collection.fluxRSS