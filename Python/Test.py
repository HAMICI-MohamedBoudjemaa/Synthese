from TF import *
from requeteMongo import *

trends = getAllTrend()

for trend in trends :
    print(trend)
    docs = getTweetByTrend(trend)
    text = ''
    nbTweets = 0
    for doc in docs:
        i = 0
        while i <= doc['retweet_count'] :
            text += (doc['tweet_text'])
            i+=1
            nbTweets+=1


    list = fiftgrams(text , nbTweets)
    print(ntop(list, 5))
    print(top(list))
    lfiftgrams = top(list)
    #setEventDescriptionByTrend(trend, top(list, 1))

    list = quadrigrams(text , nbTweets)
    print(ntop(list, 5))
    print(top(list))
    lquadrigrams = top(list)

    list = trigrams(text , nbTweets)
    print(ntop(list,5))
    print(top(list))
    ltrigrams = top(list)
    #setEventDescriptionByTrend(trend,top(list,1))

    list = bigrams(text , nbTweets)
    print(ntop(list,5))
    print(top(list))
    lbigrams = top(list)

    list = TF(text, nbTweets)
    print(ntop(list,5))
    print(top(list))
    lTF = ntop(list,5)
    ltf = top(list)
    ltf1 = ''
    for a in lTF :
        ltf1 += ' '+a

    print(chooseResult(lfiftgrams, lquadrigrams, ltrigrams, lbigrams, ltf, ltf1))
    print('***************************')