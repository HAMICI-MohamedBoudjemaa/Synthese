from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
from Python.TF import *
from Python.requeteMongo import *
from Python.GeonamesAnalyze import *

ELASTICSEARCHAUTHENTIFICATION = Elasticsearch(["https://elastic:mGK1rNCxN2eTY9c2wYNDdeAO@05d26646b8bd4fd880845957019896f4.eu-central-1.aws.cloud.es.io:9243"])
FLUXINDEX = "fluxrss-stemmed-2019.06.20"
MIMMATCHDESCRIPTION = 3
MINMATCHTITLE = 1

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
              minimum_should_match=MIMMATCHDESCRIPTION)

        flowSearch = flowSearch.query(q)
        flowSearch = flowSearch[0:3]

        response = flowSearch.execute()
        responseDict = response.to_dict()
        nbRes = responseDict['hits']['total']['value']
        if nbRes > 0:
            placeHits = responseDict['hits']['hits']
            for placeHit in placeHits:
                element = placeHit['_source']
                print('Description : ' + element['description'])
                print('Score : ' + str(placeHits['_score']))
                print('Titre: ' + element['titre'])
                print('id: ' + element['idFlux']['$oid'])
                res.append(element['idFlux']['$oid'])
    return res

def searchMultipleFluxRSS(keywords):
    res = None
    es = ELASTICSEARCHAUTHENTIFICATION
    flowSearch = Search(using=es, index=FLUXINDEX)
    shouldDescreptionQuery = []
    shouldTitleQuery = []

    if keywords:
        textSplit = keywords.split()
        for text in textSplit:
            queryDescription = Q('match', description=text)
            if queryDescription not in shouldDescreptionQuery:
                shouldDescreptionQuery.append(queryDescription)

            queryTitle = Q('match', titre=text)
            if queryTitle not in shouldTitleQuery:
                shouldTitleQuery.append(queryTitle)

        boolDescreption = Q('bool',\
              should=shouldDescreptionQuery,\
              minimum_should_match=MIMMATCHDESCRIPTION)

        boolTitle = Q('bool', \
                    should=shouldTitleQuery, \
                    minimum_should_match=MINMATCHTITLE)

        mustMainBoolQuery = [boolDescreption, boolTitle]
        boolMain = Q('bool', \
                     must = mustMainBoolQuery)

        flowSearch = flowSearch.query(boolMain)
        flowSearch = flowSearch[0:3]

        response = flowSearch.execute()
        responseDict = response.to_dict()
        nbRes = responseDict['hits']['total']['value']
        if nbRes > 0:
            placeHits = responseDict['hits']['hits']
            for placeHit in placeHits:
                element = placeHit['_source']
                print('Description : ' + element['description'])
                print('Score : ' + str(placeHit['_score']))
                print('Titre: ' + element['titre'])
                print('id: ' + element['idFlux']['$oid'])
                if res is None:
                    res = []
                res.append(element['idFlux']['$oid'])
    return res

def fluxRSS(text, nbTweets, trend):
    listKeywords = createListKeywords(text, nbTweets)
    result = chooseResult(listKeywords, 10)
    result = deleteSubstr(result)
    result = createResultText(result)
    result = deleteDuplicates(result)
    result = result.strip()  # GET RID OF THE FUCKING SPACE CHARACTER IN EVERY FUCKING LINE, WHY NO ONE ACKNOWLEDGE THAT

    trend = trend.replace('#', '')
    trendSplit = trend.split()
    for trendStr in trendSplit:
        if not result:
            result = trendStr
        else:
            result = result + ' ' + trendStr

    print('Keywords: ' + result)
    setId = searchMultipleFluxRSS(result)
    if setId is not None:
        update = events.update({'tendance': trend},
                               {'$set': {'flux_rss': setId, 'status': True}})

    print('***********FIN***RSS*FEED************\n')
