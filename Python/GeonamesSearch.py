import re
from fuzzywuzzy import fuzz
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q

FUZINESS = 90
ELASTICSEARCHAUTHENTIFICATION = Elasticsearch(["https://elastic:ZsCkeJa6qrPR6YICH8nwCRZR@487a3c18579448be987a324822344a49.eu-central-1.aws.cloud.es.io:9243"])

def searchCountryCityByName(name):
    res = None
    es = ELASTICSEARCHAUTHENTIFICATION
    geonameSearch = Search(using=es, index="geoname-2019.05.30")
    alternatenameSearch = Search(using=es, index="alternatenames-2019.05.30")
    translateSearch = alternatenameSearch.query("term", alternatename__keyword=name)
    translateSearch = translateSearch.query("term", isoLanguage__keyword='fr')
    translateSearch = translateSearch[0:10]
    response = translateSearch.execute()
    responseDict = response.to_dict()
    nbRes = responseDict['hits']['total']['value']

    if nbRes > 0:  # City or country exists
        geonameids = []
        geonameidHits = responseDict['hits']['hits']
        for geonameidHit in geonameidHits:
            geonameids.append(geonameidHit['_source']['geonameid'])
            for geonameid in geonameids:
                geonameInfoSearch = geonameSearch.query("term", geonameid__keyword=geonameid)
                geonameInfoSearch = geonameInfoSearch.query("terms", featureClass__keyword=['P', 'A'])
                geonameInfoSearch = geonameInfoSearch.exclude("match", population="0")
                geonameInfoSearch = geonameInfoSearch.exclude("match", featureCode="ADM2")
                geonameInfoSearch = geonameInfoSearch.exclude("match", featureCode="ADM4")
                geonameInfoSearch = geonameInfoSearch.exclude("match", featureCode="ADM3")
                response = geonameInfoSearch.execute()
                responseDict = response.to_dict()
                nbRes = responseDict['hits']['total']['value']
                if nbRes > 0:
                    returnHits = responseDict['hits']['hits']
                    res = []
                    for returnHit in returnHits:
                        res.append(returnHit['_source'])
    return res

def searchPlaceByName(name, dictCityCountry):
    res = None
    es = ELASTICSEARCHAUTHENTIFICATION
    geonameSearch = Search(using=es, index="geoname-2019.05.30")
    alternatenameSearch = Search(using=es, index="alternatenames-2019.05.30")

    mustQuery = [Q('term', name__keyword=name)]
    mustnotQuery = [Q('match', featureClass='P'), Q('match', featureClass='A')]
    shouldQuery = []

    if dictCityCountry['country'] is not None:
        for i in range(len(dictCityCountry['country'])):
            query = Q('match', countryCode=dictCityCountry['country'][i])
            if query not in shouldQuery:
                shouldQuery.append(query)

    if dictCityCountry['city'] is not None:
        for item in dictCityCountry['city']:
            queryCountryCode = Q('match', countryCode=item['countryCode'])
            queryAdminCode = Q('match', countryCode=item['admin2Code'])
            #shouldQuery.append(Q('match', admin2Code=item['admin2Code']))
            if queryCountryCode not in shouldQuery:
                shouldQuery.append(queryCountryCode)
            #if queryAdminCode not in shouldQuery:
            #    shouldQuery.append(queryAdminCode)

    q = Q('bool',\
          must=mustQuery,\
          should=shouldQuery,\
          must_not=mustnotQuery)

    placeSearch = geonameSearch.query(q)
    placeSearch = placeSearch.query("exists", field="admin2Code")
    placeSearch = placeSearch.query("exists", field="alternatenames")
    placeSearch = placeSearch[0:5]

    response = placeSearch.execute()
    responseDict = response.to_dict()
    nbRes = responseDict['hits']['total']['value']
    if nbRes > 0:
        placeHits = responseDict['hits']['hits']
        #print(placeHits)
        for i in range(len(placeHits)):
            placeHit = placeHits[i]['_source']
            fuziness = fuzz.ratio(name, placeHit['name'])
            if fuziness > FUZINESS and placeHit['admin2Code'] is not None:
                if res is None:
                    res = []
                res.append(placeHit)

    if res is None:
        popularPlace = alternatenameSearch.query('match', alternatename=name)
        popularPlace = popularPlace.query("term", isoLanguage__keyword='fr')
        popularPlace = popularPlace[0:1]
        response = popularPlace.execute()
        responseDict = response.to_dict()
        nbRes = responseDict['hits']['total']['value']
        if nbRes > 0:
            placeHits = responseDict['hits']['hits']
            for placeHit in placeHits:
                if res is None:
                    res = []
                fuziness = fuzz.ratio(placeHit['_source']['alternatename'], name)
                if fuziness > FUZINESS:
                    found = searchAllByGeonameid(placeHit['_source']['geonameid'])
                    if found is not None:
                        res.append(found)
    return res

def searchCityByCode(code):
    es = Elasticsearch(
        ["https://elastic:ZsCkeJa6qrPR6YICH8nwCRZR@487a3c18579448be987a324822344a49.eu-central-1.aws.cloud.es.io:9243"])
    s = Search(using=es, index="admincode-2019.05.30")
    s = s.query("term", code__keyword = code)

    response = s.execute()
    responseDict = response.to_dict()

    res = None
    nbRes = responseDict['hits']['total']['value']
    if nbRes > 0:
        res = responseDict['hits']['hits'][0]['_source']['name']
    return res

def searchAllByGeonameid(geonameid):
    es = ELASTICSEARCHAUTHENTIFICATION
    geonameSearch = Search(using=es, index="geoname-2019.05.30")
    geonameSearch = geonameSearch[0:5]
    geonameSearch = geonameSearch.query("match", geonameid=geonameid)
    geonameSearch = geonameSearch.query("exists", field="admin2Code")
    geonameSearch = geonameSearch.exclude("match", featureClass="A")
    geonameSearch = geonameSearch.exclude("match", featureClass="P")

    response = geonameSearch.execute()
    responseDict = response.to_dict()
    found = None

    nbRes = responseDict['hits']['total']['value']
    if nbRes > 0:
        found = responseDict['hits']['hits'][0]['_source']
    return found

def searchCityNameByCode(code):
    es = Elasticsearch(
        ["https://elastic:ZsCkeJa6qrPR6YICH8nwCRZR@487a3c18579448be987a324822344a49.eu-central-1.aws.cloud.es.io:9243"])
    s = Search(using=es, index="admincode-2019.05.28")
    s = s[0:5]
    s = s.query("match", code=code)


    response = s.execute()
    responseDict = response.to_dict()
    found = None

    nbRes = responseDict['hits']['total']['value']
    if nbRes > 0:
        found = responseDict['hits']['hits'][0]['_source']['name']
    return found

def searchContinentByISO(iso):
    res = None

    if res is None:
        es = ELASTICSEARCHAUTHENTIFICATION
        s = Search(using=es, index="countryinfo-2019.05.30")
        s = s[0:5]
        s = s.query("term", ISO__keyword=iso)

        response = s.execute()
        responseDict = response.to_dict()
        nbRes = responseDict['hits']['total']['value']
        if nbRes > 0:
            res = responseDict['hits']['hits'][0]['_source']['continent']
    return res