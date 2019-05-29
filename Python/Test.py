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


    list5 = fiftgrams(text , nbTweets)
    print(ntop(list5, 5))
    print(top(list5))
    lfiftgrams = top(list5)
    #setEventDescriptionByTrend(trend, top(list, 1))

    list4 = quadrigrams(text , nbTweets)
    print(ntop(list4, 5))
    print(top(list4))
    lquadrigrams = top(list4)

    list3 = trigrams(text , nbTweets)
    print(ntop(list3,5))
    print(top(list3))
    ltrigrams = top(list3)
    #setEventDescriptionByTrend(trend,top(list,1))

    list2 = bigrams(text , nbTweets)
    print(ntop(list2,5))
    print(top(list2))
    lbigrams = top(list2)

    list1 = TF(text, nbTweets)
    print(ntop(list1,5))
    print(top(list1))
    lTF = top(list1)

    print(chooseResult(lfiftgrams, lquadrigrams, ltrigrams, lbigrams, lTF))
    print('***************************')