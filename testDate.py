from Python.requeteMongo import getAllTrend
from Python.requeteMongo import getTweetByTrend
from getdate import *

trends = getAllTrend()

for trend in trends :
    print(trend)
    docs = getTweetByTrend(trend)
    text = ''
    for doc in docs:
        i = 0
        while i <= doc['retweet_count'] :
            text += (doc['tweet_text'])
            i+=1


    date_event = getDate(text)
    print(date_event)

    print()
    print('***************************')