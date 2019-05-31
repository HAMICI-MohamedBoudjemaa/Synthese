from TF import *
from requeteMongo import *
from getdate import *
import textdistance

trends = getAllTrend()

for trend in trends :
    print(trend)
    docs = getTweetByTrend(trend)
    docs1 = getTweetByTrend(trend)
    docs2 = getTweetByTrend(trend)
    text = ''
    nbTweets = 0

    for doc in docs:
        i = 0
        if (doc['followers'] > 100000 and doc['retweet_count']>5 and percentageBadOrthograph(doc['tweet_text'])<0.3) :
            while i <= doc['retweet_count'] :
                text += (doc['tweet_text'])
                i+=1
                nbTweets+=1

    #find keywords
    listKeywords = createListKeywords(text,nbTweets)
    result = chooseResult(listKeywords,5)
    print('del')
    result = deleteSubstr(result)
    result = createResultText(result)
    print(result)

    #find rss article
    print('resultat flux rss : ' + searchTextInTitleFluxRSS(result))

    #find representative tweet
    representativeTweet = selectRepresentativeTweet(result, docs1)
    print('tweet representatif : '+representativeTweet)
    #setEventDescriptionByTrend(trend, top(list, 1))

    #print(text)
    #date_event = getDate2(docs2)
    #print("date event " + date_event)
    print('***************************')