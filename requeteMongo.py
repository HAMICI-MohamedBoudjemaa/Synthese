from connexionMongoBis import tweets

"""
retourne les tweets d'une tendance renseigné
"""
def getTweetByTrend(trend):
    return tweets.find({'tendance': trend})

"""
retourne toutes les tendances de l'évenement (collectioon : events)
"""
def getAllTrend():
    return tweets.find()


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

if __name__ == '__main__':
    i = 0
    for doc in getTweetByTrend('#Tech4Good'):
        print(doc['hashtags'][0]['text'])
        i = i +1
    print(i)


