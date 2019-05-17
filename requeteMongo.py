from connexionMongoBis import *

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
        i = 0
        for tend in trend:
            tweet = tend['tweet_text']
            tweet_text.append(tweet)
            i = i +1
            result = ' '.join(tweet_text)
        print("total {} {}".format(tr,i))
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
if __name__ == '__main__':
   """ i = 0
    for doc in getTweetByTrend('#Tech4Good'):
        print(doc['hashtags'][0]['text'])
        i = i +1
    print(i)"""
   #print(getAllTrend())
   #print(getTweetAllTrend())
   for t in getTweetByTrend("#VivaTech"):
        print(t['tweet_text'])

