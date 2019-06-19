from Python.TF import *
from Python.requeteMongo import *
from getdate import *
from Python.GeonamesAnalyze import *
import textdistance
from Python.requeteMongo import *
from Python.fluxElastic import *

trends = getAllTrend()

nbtrends = 0
for trend in trends :
    print('Tendance: {}'.format(trend))
    nbtrends+=1
    if nbtrends==100:
        break
    docsdate, docs = getTweetByTrend(trend)
    #docs1 = getTweetByTrend(trend)
    text = ''
    nbTweets = 0
    for doc in docs:
        i = 0

        if (doc['followers'] > 100000 and doc['retweet_count']>5 and percentageBadOrthograph(doc['tweet_text'])<0.3) :
            while i <= doc['retweet_count'] :
                text += '. '+(doc['tweet_text'])
                i+=1
                nbTweets+=1
    #print(nbtrends)
    #f = open("/Users/phucvu/Desktop/testText.txt", "w")
    #f.write(text)

    tweetDescription(text, nbTweets, docs, trend)
    tweetPlace(text, trend)
    fluxRSS(text, nbTweets, trend)
    datef = getDate2(docsdate)
    setEventDateByTrend(trend, datef):
    print('*********************$$$***************************')