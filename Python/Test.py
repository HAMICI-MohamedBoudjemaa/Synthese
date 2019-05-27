from TF import *
from requeteMongo import *

trends = getAllTrendIfStatusIsFalse()

for trend in trends :
    print(trend)
    docs = getTweetByTrend(trend)
    text = ''
    for doc in docs:
        i = 0
        while i < doc['retweet_count'] :
            text += (doc['tweet_text'])
            i+=1


    list = ninegrams(text)
    print(top(list, 5))

    list = eightgrams(text)
    print(top(list, 5))

    list = sevengrams(text)
    print(top(list, 5))
    #setEventDescriptionByTrend(trend, top(list, 1))

    list = sixgrams(text)
    print(top(list, 5))
    #setEventDescriptionByTrend(trend, top(list, 1))

    list = fiftgrams(text)
    print(top(list, 5))
    setEventDescriptionByTrend(trend, top(list, 1))

    list = quadrigrams(text)
    print(top(list, 5))

    list = trigrams(text)
    print(top(list,5))
    #setEventDescriptionByTrend(trend,top(list,1))

    list = bigrams(text)
    print(top(list,5))

    list = TF(text)
    print(top(list,5))
    print('***************************')