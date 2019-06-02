import re
from fuzzywuzzy import fuzz
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
import numpy as np
from heapq import nlargest
from Python.Place import *

THRESHOLD_KEYWORD = 2
FUZINESS = 85
TOPHITS = 3
ELASTICSEARCHAUTHENTIFICATION = Elasticsearch(["https://elastic:ZsCkeJa6qrPR6YICH8nwCRZR@487a3c18579448be987a324822344a49.eu-central-1.aws.cloud.es.io:9243"])

def searchCountryCityByName(name):
    res = None
    es = ELASTICSEARCHAUTHENTIFICATION
    geonameSearch = Search(using=es, index="geoname-2019.05.30")
    alternatenameSearch = Search(using=es, index="alternatenames-2019.05.30")
    translateSearch = alternatenameSearch.query("term", alternatename__keyword=name)
    translateSearch = translateSearch.query("term", isoLanguage__keyword='fr')
    translateSearch = translateSearch[0:3]
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
            shouldQuery.append(Q('match', countryCode=dictCityCountry['country'][i]))
    if dictCityCountry['city'] is not None:
        for item in dictCityCountry['city']:
            shouldQuery.append(Q('match', admin2Code=item['admin2Code']))
            shouldQuery.append(Q('match', countryCode=item['countryCode']))

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
        for i in range(len(placeHits)):
            placeHit = placeHits[i]['_source']
            fuziness = fuzz.ratio(name, placeHit['name'])
            if fuziness > FUZINESS and placeHit['admin2Code'] is not None:
                if res is None:
                    res = []
                res.append(placeHit)

    if res is None:
        popularPlace = alternatenameSearch.query('match', alternatename__keywordl=name)
        popularPlace = popularPlace.query("term", isoLanguage__keyword='fr')
        popularPlace = popularPlace[0:3]
        response = popularPlace.execute()
        responseDict = response.to_dict()
        nbRes = responseDict['hits']['total']['value']
        if nbRes > 0:
            placeHits = responseDict['hits']['hits']
            for placeHit in placeHits:
                if res is None:
                    res = []
                found = searchAllByGeonameid(placeHit['_source']['geonameid'])
                if found is not None:
                    res.append(found)

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

def textProcessing(text):
    text = re.sub(r'\-', ' ', text)
    text = re.sub(r'\"', '', text)
    text = re.sub(r'\.\s*(?=)[A-Z]', lambda m: m.group().lower(), text)  # cute. This is a phrase -> cute. this is..
    text = re.sub(r'\?\s*(?=)[A-Z]', lambda m: m.group().lower(), text)  # cute? This is a phrase -> cute. this is..
    text = re.sub(r'\!\s*(?=)[A-Z]', lambda m: m.group().lower(), text)  # cute? This is a phrase -> cute. this is..
    text = re.sub(r'\:\s*(?=)[A-Z]', lambda m: m.group().lower(), text)  # cute? This is a phrase -> cute. this is..
    text = re.sub(r'\;\s*(?=)[A-Z]', lambda m: m.group().lower(), text)  # cute? This is a phrase -> cute. this is..
    #text = re.sub(r'\W\s*(?=)[A-Z]', lambda m: m.group().lower(), text)  # cute! This is a phrase -> cute. this is..
    #text = re.sub('^\s*[A-Z]', lambda m: m.group().lower(), text, flags=re.M)
    placeDict = dict()
    placeRegex = re.compile(r'([A-Z][A-Za-z]+(\s+[A-Z][a-z]+)*)')
    hashtagRegex = re.compile(r'\#[A-Za-z0-9]*')
    places = placeRegex.findall(text)
    hashtags = hashtagRegex.findall(text)

    for place in places:
        place = place[0].strip()
        place = re.sub(r'\bThe\b', '', place)
        place = re.sub(r'\bLe\b', '', place)
        place = re.sub(r'\bLa\b', '', place)
        place = re.sub(r'\bL\'\b', '', place)
        place = re.sub(r'\bUn\b', '', place)
        place = re.sub(r'\bUne\b', '', place)
        place = re.sub(r'\bTa\b', '', place)
        place = re.sub(r'\bTon\b', '', place)
        place = re.sub(r'\bVotre\b', '', place)
        place = re.sub(r'\bSon\b', '', place)
        place = re.sub(r'\bSes\b', '', place)
        if place.isupper():  # WASHINGTON -> #Washington
             place = place.lower()
             place = place.capitalize()
        place = place.strip()
        if place in placeDict:
            placeDict[place] += 1
        else:
            placeDict[place] = 1

    for hashtag in hashtags:
        hashtag = hashtag.replace('#', '')
        if re.search('^[a-z].*', hashtag):
            hashtag = hashtag.capitalize()  # notredame -> Notredame

        if hashtag in placeDict:
            placeDict[hashtag] += 1
        else:
            placeDict[hashtag] = 1

    newPlaceDict = dict()
    for key,value in placeDict.items():
        if value > THRESHOLD_KEYWORD:
            newPlaceDict[key] = value
    placeDict = newPlaceDict
    del(newPlaceDict)
    return placeDict

def analyze(str):
    cityDict = dict()
    countryDict = dict()
    placeDict = dict()

    cityTopCountDict = None
    countryTopCountDict = None
    placeTopCountDict = None

    resultDict = dict()
    resultDict['country'] = None
    resultDict['city'] = None
    resultDict['place'] = None

    extractedCityCountry = textProcessing(str)
    extractedPlace = []
    dictCityCountry = dict()
    dictCityCountry['country'] = None
    dictCityCountry['city'] = None

    if extractedCityCountry is not None:
        for extractedItem in extractedCityCountry:
            arrayCityCountry = searchCountryCityByName(extractedItem)

            if arrayCityCountry is not None:
                if arrayCityCountry[0]['featureClass'] == 'A':
                    type = 'Country'
                elif arrayCityCountry[0]['featureClass'] == 'P':
                    type = 'City'

                if type == 'Country':
                    countryTopCountDict = dict()
                    if dictCityCountry['country'] is None:
                        dictCityCountry['country'] = []
                    for item in arrayCityCountry:
                        placeObject = Place()
                        placeObject.name = item['name']
                        placeObject.type = 'Pays'
                        placeObject.ofCountry = item['countryCode']
                        #countryDict[extractedItem]['count'] = extractedCityCountry[extractedItem]
                        countryDict[extractedItem] = placeObject
                        countryTopCountDict[extractedItem] = extractedCityCountry[extractedItem]
                        dictCityCountry['country'].append(item['countryCode'])

                if type == 'City':
                    cityTopCountDict = dict()
                    if dictCityCountry['city'] is None:
                        dictCityCountry['city'] = []
                    for item in arrayCityCountry:
                        placeObject = Place()
                        placeObject.name = item['name']
                        placeObject.type = 'Ville'
                        placeObject.ofCountry = item['countryCode']
                        #cityDict[extractedItem]['count'] = extractedCityCountry[extractedItem]
                        cityDict[extractedItem] = placeObject
                        cityTopCountDict[extractedItem] = extractedCityCountry[extractedItem]
                        dictCityCountry['city'].append({'countryCode':item['countryCode'],\
                                                        'admin2Code':item['admin2Code']})

            else:
                extractedPlace.append([extractedItem,extractedCityCountry[extractedItem]])

        for place in extractedPlace:
            placename = place[0]
            arrayPlace = searchPlaceByName(placename, dictCityCountry)

            if arrayPlace is not None:
                placeTopCountDict = dict()
                for item in arrayPlace:
                    placeObject = Place()
                    placeObject.name = item['name']
                    placeObject.ofCountry = item['countryCode']
                    placeObject.ofCity = item['countryCode'] + "." + item['admin1Code'] + "." + item['admin2Code']
                    placeDict[place] = placeObject
                    placeTopCountDict[extractedItem] = extractedCityCountry[place]

        if countryTopCountDict is not None:
            topCountry = nlargest(TOPHITS, countryTopCountDict, countryTopCountDict.get)
            resultDict['country'] = dict()
            for country in topCountry:
                resultDict['country'][country] = [countryTopCountDict[country], countryDict[country]]
        if cityTopCountDict is not None:
            topCity = nlargest(TOPHITS, cityTopCountDict, cityTopCountDict.get)
            resultDict['city'] = dict()
            for city in topCity:
                resultDict['city'][city] = [cityTopCountDict[city], cityDict[city]]
        if placeTopCountDict is not None:
            topPlace = nlargest(TOPHITS, placeTopCountDict, placeTopCountDict.get)
            resultDict['place'] = dict()
            for place in placeDict:
                resultDict['place'][place] = [placeTopCountDict[place], topPlace[place]]

    return resultDict

def showResult(arrayResult):

    if arrayResult['country'] is not None:
        print('******************************************************')
        print('*                    Pays trouvés                    *')
        print('******************************************************')
        for country in arrayResult['country']:
            count = arrayResult['country'][country][0]
            info = arrayResult['country'][country][1]
            print('* [{}] apparait {} fois dans le document'.format(country, count))
            print('* [{}] Code Pays: {}'.format(country, info.ofCountry))
        print('******************************************************')
        print('\n')
    else:
        print('******************************************************')
        print('*          Pas d\'information pour les pays          *')
        print('******************************************************')
        print('\n')

    if arrayResult['country'] is not None:
        print('******************************************************')
        print('*                   Villes trouvés                   *')
        print('******************************************************')
        for city in arrayResult['city']:
            count = arrayResult['city'][city][0]
            info = arrayResult['city'][city][1]
            print('* [{}] apparait {} fois dans le document'.format(city, count))
            print('* [{}] Code Pays: {}'.format(city, info.ofCountry))
        print('******************************************************')
        print('\n')
    else:
        print('******************************************************')
        print('*         Pas d\'information pour les villes         *')
        print('******************************************************')
        print('\n')


    if arrayResult['place'] is not None:
        print('******************************************************')
        print('*                   Lieux trouvés                    *')
        print('******************************************************')
        for place in arrayResult['place']:
            place = arrayResult['place'][place][0]
            info = arrayResult['place'][place][1]
            print('* [{}] apparait {} fois dans le document'.format(place, count))
            print('* [{}] Code Pays: {}'.format(place, info.ofCountry))
            print('* [{}] Villes: {}'.format(place, searchCityByCode(info.ofCity)))
        print('******************************************************')
        print('\n')
    else :
        print('******************************************************')
        print('*         Pas d\'information pour les lieux          *')
        print('******************************************************')
        print('\n')




















