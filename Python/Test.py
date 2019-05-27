from TF import *
from requeteMongo import *

trends = getAllTrend()

for trend in trends :
    print(trend)
    docs = getTweetByTrend(trend)
    text = ''
    for doc in docs:
        text += (doc['tweet_text'])

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
    #setEventDescriptionByTrend(trend, top(list, 1))

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