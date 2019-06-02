import pymongo
#from connnexionMongo import *

from connnexionMongo import *

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
        tr = trend['tendance']
        tendances.append(tr)
    return tendances

"""
retourne toutes les tendances de la collection events 
"""
def getAllTrend():
    q= events.find()
    tendances = []
    for trend in q:
        tr = trend['tendance']
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
    update = events.update({'tendance':trend}, {'$set':{'description':description, 'status':True}})
    return update
"""
Ajoute le lieu à chaque doc de la collection events
trend : tendence
lieu : le lieu
"""
def setEventLieuByTrend(trend, lieu):
    update = events.update({'tendance':trend}, {'$set':{'lieu':lieu}})
    return update

"""
Ajoute la date à chaque doc de la collection events
trend : tendence
date : la date
"""
def setEventDateByTrend(trend, date):
    update = events.update({'tendance':trend}, {'$set':{'date':date}})
    return update


"""
Mets à jours les champs vide de la collection events(description, lieu, date, status)
"""
def setFieldEventByTrend(trend, description, lieu, date):
    update = events.update({'tendance': trend}, {'$set': {'description': description, 'lieu':lieu, 'date':date, 'status':True}})
    return update

"""
retourne le nombre de tweets, nombre retweets,  nombre utilisateur et la date du premier tweet d'une tendance données
"""
def getCountElementTrend(trend):
    rt = [{"$match": {"tendance": trend}},
          {"$group": {"_id": "$tendance",
                      "date_premier_tweet": { "$min": "$created"},
                      "nombre_retweet": {"$sum": "$retweet_count"},
                      "nb_user": {"$sum": 1}
                     }
          }
         ]


    cursor = tweets.aggregate(rt)
    result = list(cursor)
    rs = {"nb_tw": getTweetByTrend(trend).count(),
          "nb_rt":result[0]['nombre_retweet'],
          "nb_user":result[0]['nb_user'],
          "date_premier_tweet":result[0]['date_premier_tweet']}

    return rs

"""
Recherche un text dans le Titre du flux RSS, trie par ordre score
et retourne le titre ayant le plus grand score
"""
def searchTextInTitleFluxRSS(search_text):
    array = []
    cursor = fluxRSS.find(
        {'$text': {'$search': search_text}},
        {'score': {'$meta': 'textScore'}}
    )
    # Sort by 'score' field.
    cursor.sort([('score', {'$meta': 'textScore'})])
    for doc in cursor:
        array.append(doc)
    if not array:
        return ''
    else:
        print(array[0]['description'])
        return array[0]['titre']

"""
cherche si un tweet existe à partir de l'id du tweet
"""
def findIfTweetIdExist(tweet_id):
     id_tweet = list(tweets.find({"tweet_id":tweet_id}).limit(1))
     return len(id_tweet)

"""
mets à jour à partir de l'id du tweet le nombre de followers,
 nombre de tweets et de like d'un tweet 
"""
def updateTweets(tweet_id,followers, retweet_count, favorite_count):
    update = tweets.update(
        {'tweet_id': tweet_id},
        {'$set': {'followers':followers,
                  'retweet_count':retweet_count,
                   'favorite_count':favorite_count
                }
        }
    )
    return update

"""
cherche si une tendance existe dans la collection <<events>> 
"""
def findIfEventExist(trend):
    tendance = list(events.find({"tendance": trend}).limit(1))
    return len(tendance)


#Structure champs collection tweets
""""
    tendance
    tweet_id
    user_id
    username
    screen_name
    followers
    description
    tweet_text
    hashtags
    userLocation
    retweet_count
    favorite_count
    retweeted
    created
"""

#Structure champs collection events
""""
    tendance
    description
    lieu 
    date
    status
"""

#Structure collection fluxRSS
"""
tendance
description
lieu
date
status
False
flux_rss
tweets_representatifs
"""
if __name__ == '__main__':
    print(searchTextInTitleFluxRSS("Darmanin et Sébastien"))
    #fluxRSS.create_index([("titre, descrption", pymongo.TEXT)])
    #tweets.create_index([("tweet_id", "unique=True")])
    #tweets.create_index("tweet_id", unique=True)
    #fluxRSS.create_index([("titre", pymongo.TEXT), ("description", pymongo.TEXT)])


