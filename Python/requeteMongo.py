import datetime

from Python.connexionLocal import *

"""
à partir d'une tendance renseigné recupère tous les documents lui correspondant
dans la collection tweets
"""
def getTweetByTrend(trend):
    return tweets.find({'tendance': trend})

"""
renvoie toutes les tendances de la collection events non traités (tendance -> champs id, status -> false)
"""
def getAllTrendIfStatusIsFalse():
    q= events.find({'status':False})
    tendances = []
    for trend in q:
        tr = trend['id']
        tendances.append(tr)
    return tendances

"""
retourne toutes les tendances de la collection events 
"""
def getAllTrend():
    q= events.find()
    tendances = []
    for trend in q:
        tr = trend['id']
        tendances.append(tr)
    return tendances

"""
retourne tous les tweets de chaque tendance 
"""
def getTweetByTrends():
    for tr in getAllTrendIfStatusIsFalse():
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
    update = events.update({'id':trend}, {'$set':{'description':description, 'status':True}})
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


"""
Mets à jours les champs vide de la collection events(description, lieu, date, status)
"""
def setFieldEventByTrend(trend, description, lieu, date):
    date = datetime.datetime.strptime(date, '%d/%m/%Y')
    update = events.update({'id': trend}, {'$set': {'description': description, 'lieu':lieu, 'date':date, 'status':True}})
    return update

def getCountTweet_text(trend):
    cpt = tweets.find({"tendance": trend}).count()
    return cpt

def getRetweet_count(trend):
    rt = [{"$match": {"tendance": trend}},
          {"$group": {"_id": "$tendance",
                      "date_premier_tweet": { "$min": "$created"},
                      "nombre_retweet": {"$sum": "$retweet_count"},
                      "nb_user": {"$sum": 1}
        }}]


    cursor = tweets.aggregate(rt)
    result = list(cursor)
    rs = {"nb_tw": getCountTweet_text(trend),
          "nb_rt":result[0]['nombre_retweet'],
          "nb_user":result[0]['nb_user'],
          "date_premier_tweet":result[0]['date_premier_tweet'],}

    return rs



#Structure champs collection tweets
""""
    "tendance" 
    "tweet_id" 
    "id_user" 
    "username" 
    "screen_name" 
    "followers" 
    "description" 
    "tweet_text" :
    "hashtags":  ['hashtags'][indice]['text']
    "userLocation": 
    "retweet_count": 
    "created": 
"""

#Structure champs collection events
""""
    "id" -> tendance 
    "description"
    "lieu" 
    "date" 
    "status" 
"""

if __name__ == '__main__':
    print(getRetweet_count("#MondayMotivation"))
