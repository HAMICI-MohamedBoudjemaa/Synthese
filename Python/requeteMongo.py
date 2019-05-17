"""
retourne les tweets d'une tendance renseigné
"""
from connnexionMongo import *

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

"""
Ajoute la description à chaque doc de la collection events
trend : tendence
description : la description
"""
def setEventDescriptionByTrend(trend, description):
    update = events.update({'id':trend}, {'$set':{'description':description}})
    return update

"""
Ajoute le lieu à chaque doc de la collection events
trend : tendence
lieu : le lieu
"""
def setEventLieuByTrend(trend, lieu):
    update = events.update({'id':trend}, {'$set':{'lieu':lieu}})
    return update

"""
Ajoute la date à chaque doc de la collection events
trend : tendence
date : la date
"""
def setEventDateByTrend(trend, date):
    date = datetime.datetime.strptime(date,  '%d/%m/%Y')
    update = events.update({'id':trend}, {'$set':{'date':date}})
    return update

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
