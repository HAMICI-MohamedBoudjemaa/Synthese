from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
from Python.TF import *
from Python.requeteMongo import *

ELASTICSEARCHAUTHENTIFICATION = Elasticsearch(["https://elastic:mGK1rNCxN2eTY9c2wYNDdeAO@05d26646b8bd4fd880845957019896f4.eu-central-1.aws.cloud.es.io:9243"])
FLUXINDEX = "fluxrss-stemmed-2019.06.16"
MIMMATCH = 4

def searchTextInTitleFluxRSS(search_text):
    res = None
    es = ELASTICSEARCHAUTHENTIFICATION
    flowSearch = Search(using=es, index=FLUXINDEX)
    mustQuery = []
    shouldQuery = []
    mustnotQuery = []


    if search_text:
        textSplit = search_text.split()
        for text in textSplit:
            queryTitle = Q('match', titre=text)
            queryDescription = Q('match', description=text)
            if queryTitle not in shouldQuery:
                shouldQuery.append(queryTitle)
            if queryDescription not in shouldQuery:
                shouldQuery.append(queryDescription)

        q = Q('bool',\
              must=mustQuery,\
              should=shouldQuery,\
              must_not=mustnotQuery,\
              minimum_should_match=MIMMATCH)

        flowSearch = flowSearch.query(q)
        flowSearch = flowSearch[0:1]

        response = flowSearch.execute()
        responseDict = response.to_dict()
        nbRes = responseDict['hits']['total']['value']
        if nbRes > 0:
            placeHits = responseDict['hits']['hits']
            i = 0
            placeHit = placeHits[i]['_source']
            print('Description : ' + placeHit['description'])
            print('Score : ' + str(placeHits[i]['_score']))
            print('Titre: ' + placeHit['titre'])
            res = placeHit['titre']
    return res

if __name__ == '__main__':
    trends = getAllTrend()
    for trend in trends:
        print('Trend: ' + trend)
        docs = getTweetByTrend(trend)
        text = ''
        nbTweets = 0
        for doc in docs:
            i = 0
            if (doc['followers'] > 100000 and doc['retweet_count'] > 5 and percentageBadOrthograph(
                    doc['tweet_text']) < 0.3):
                while i <= doc['retweet_count']:
                    text += '. ' + (doc['tweet_text'])
                    i += 1
                    nbTweets += 1

        listKeywords = createListKeywords(text, nbTweets)
        result = chooseResult(listKeywords, 10)
        result = deleteSubstr(result)
        result = createResultText(result)
        result = deleteDuplicates(result)
        result = result.strip() #GET RID OF THE FUCKING SPACE CHARACTER IN EVERY FUCKING LINE, WHY NO ONE ACKNOWLEDGE THAT

        trend = trend.replace('#', '')
        trendSplit = trend.split()
        for trendStr in trendSplit:
            if not result:
                result = trendStr
            else :
                result = result + ' ' + trendStr

        print('Keywords: ' + result)
        searchTextInTitleFluxRSS(result)
        print('*****************************\n')
