from TF import *
from requeteMongo import *
from getdate import *
import textdistance

trends = getAllTrend()

for trend in trends :
    print(trend)
    docs = getTweetByTrend(trend)
    docs1 = getTweetByTrend(trend)
    text = ''
    nbTweets = 0

    for doc in docs:
        i = 0
        if (doc['followers'] > 100000 and doc['retweet_count']>5 and percentageBadOrthograph(doc['tweet_text'])<0.3) :
            while i <= doc['retweet_count'] :
                text += (doc['tweet_text'])
                i+=1
                nbTweets+=1

    tweetDescription(text, nbTweets, docs1)