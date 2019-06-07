from TF import *
from requeteMongo import *
from getdate import *
from GeonamesAnalyze import *
import textdistance

trends = getAllTrend()

nbtrends = 0
for trend in trends :
    print(trend)
    nbtrends+=1
    if nbtrends==99:
        break
    docs = getTweetByTrend(trend)
    docs1 = getTweetByTrend(trend)
    text = ''
    nbTweets = 0
    for doc in docs:
        i = 0

        if (doc['followers'] > 100000 and doc['retweet_count']>5 and percentageBadOrthograph(doc['tweet_text'])<0.3) :
            while i <= doc['retweet_count'] :
                text += ' '+(doc['tweet_text'])
                i+=1
                nbTweets+=1
    print(nbtrends)

    tweetDescription(text, nbTweets, docs1, trend)
    #temp=analyze(text)
    #showResult(temp)
    #analyzeResult(temp)
    #print('****************************************************')