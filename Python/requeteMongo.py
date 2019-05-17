<<<<<<< HEAD:Python/requeteMongo.py

"""
retourne les tweets d'une tendance renseigné
"""
from connnexionMongo import *


=======
from connexionMongoBis import *

>>>>>>> master:requeteMongo.py
def getTweetByTrend(trend):
    return tweets.find({'tendance': trend})

def getAllTrend():
    q= events.find()
    tendance = []
    for trend in q:
        tr = trend['id']
        tendance.append(tr)
    return tendance

def getTweetAllTrend():
    for tr in getAllTrend():
        trend = getTweetByTrend(tr)
        tweet_text =[]
        for tend in trend:
            tweet = tend['tweet_text']
            tweet_text.append(tweet)
            result = ' '.join(tweet_text)
    return result

#Structure champs monfo
""""
    "tendance" :
    "tweet_id" :
    "id_user" :
    "username" :
    "screen_name" :
    "followers" :
    "description" :
    "tweet_text" : 
    "hashtags":  ['hashtags'][indice]['text']
    "userLocation": 
    "retweet_count": 
    "created": 
"""

