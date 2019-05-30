import re
from fuzzywuzzy import fuzz
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import numpy as np
from Python.Place import *

def translateCountry(name):
    res = None
    #if len(name) == 2 and name.isupper():
    #    res = searchGeoidCountryByISO(name)
    if res is None:
        es = Elasticsearch(
            ["https://elastic:abQ4dELdOF6BDjxlotnF8JPW@a6e8c7481efc4507a806032397318270.eu-central-1.aws.cloud.es.io:9243"])
        s = Search(using=es, index="alternatenames-2019.05.17")
        s = s.query("term", alternatename__keyword = name)
        s = s.query("term", isoLanguage__keyword='fr')

        response = s.execute()
        responseDict = response.to_dict()

        nbRes = responseDict['hits']['total']['value']
        if nbRes > 0:
            geonameid = responseDict['hits']['hits'][0]['_source']['geonameid']
            s = Search(using=es, index="countryinfo-2019.05.27")
            s = s.query("term", geonameid__keyword=geonameid)
            response = s.execute()
            responseDict = response.to_dict()
            nbRes = responseDict['hits']['total']['value']
            if nbRes > 0:
                res = geonameid
    return res

def searchCityByCode(code):
    es = Elasticsearch(
        ["https://elastic:abQ4dELdOF6BDjxlotnF8JPW@a6e8c7481efc4507a806032397318270.eu-central-1.aws.cloud.es.io:9243"])
    s = Search(using=es, index="admincode-2019.05.28")
    s = s.query("term", code__keyword = code)

    response = s.execute()
    responseDict = response.to_dict()

    res = None
    nbRes = responseDict['hits']['total']['value']
    if nbRes > 0:
        res = responseDict['hits']['hits'][0]['_source']['name']
    return res


def searchGeoidCountryByName(name):
    res = None
    #if len(name) == 2 and name.isupper():
    #    res = searchGeoidCountryByISO(name)

    if res is None:
        es = Elasticsearch(
            ["https://elastic:abQ4dELdOF6BDjxlotnF8JPW@a6e8c7481efc4507a806032397318270.eu-central-1.aws.cloud.es.io:9243"])
        s = Search(using=es, index="countryinfo-2019.05.27")
        s = s[0:5]
        s = s.query("match", Country=name)

        response = s.execute()
        responseDict = response.to_dict()

        nbRes = responseDict['hits']['total']['value']
        if nbRes > 0:
            countryName = responseDict['hits']['hits'][0]['_source']['Country']
            fuziness = fuzz.ratio(name, countryName)
            if fuziness > 90:
                res = responseDict['hits']['hits'][0]['_source']['geonameid']
    return res

def searchGeoidCountryByISO(iso):
    es = Elasticsearch(
        ["https://elastic:abQ4dELdOF6BDjxlotnF8JPW@a6e8c7481efc4507a806032397318270.eu-central-1.aws.cloud.es.io:9243"])
    s = Search(using=es, index="countryinfo-2019.05.27")
    s = s[0:5]
    s = s.query("match", ISO=iso)

    response = s.execute()
    responseDict = response.to_dict()

    res = None
    nbRes = responseDict['hits']['total']['value']
    if nbRes > 0:
        res = responseDict['hits']['hits'][0]['_source']['geonameid']
    return res

def searchNameCountryByISO(iso):
    es = Elasticsearch(
        ["https://elastic:abQ4dELdOF6BDjxlotnF8JPW@a6e8c7481efc4507a806032397318270.eu-central-1.aws.cloud.es.io:9243"])
    s = Search(using=es, index="countryinfo-2019.05.27")
    s = s[0:5]
    s = s.query("match", ISO=iso)

    response = s.execute()
    responseDict = response.to_dict()

    res = None
    nbRes = responseDict['hits']['total']['value']
    if nbRes > 0:
        res = responseDict['hits']['hits'][0]['_source']['Country']
    return res

def searchAllByGeonameid(geonameid):
    es = Elasticsearch(
        ["https://elastic:abQ4dELdOF6BDjxlotnF8JPW@a6e8c7481efc4507a806032397318270.eu-central-1.aws.cloud.es.io:9243"])
    s = Search(using=es, index="geoname-2019.05.16")
    s = s[0:5]
    s = s.query("match", geonameid=geonameid)

    response = s.execute()
    responseDict = response.to_dict()
    found = None

    nbRes = responseDict['hits']['total']['value']
    if nbRes > 0:
        found = responseDict['hits']['hits'][0]['_source']
    return found

def searchCityNameByCode(code):
    es = Elasticsearch(
        ["https://elastic:abQ4dELdOF6BDjxlotnF8JPW@a6e8c7481efc4507a806032397318270.eu-central-1.aws.cloud.es.io:9243"])
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

def searchGeoidPlaceByName(name):
    es = Elasticsearch(
        ["https://elastic:abQ4dELdOF6BDjxlotnF8JPW@a6e8c7481efc4507a806032397318270.eu-central-1.aws.cloud.es.io:9243"])
    s = Search(using=es, index="geoname-2019.05.16")
    s = s.query("match", name=name)
    #s = s.query("exists", field="alternatenames")
    s = s.query("exists", field="admin1Code")
    s = s[0:5]
    #s = s.sort({"_script": {
    #     "script": "doc['alternatenames.keyword'].size()",
    #     "type": "number",
    #     "order": "asc"
    #  }
   #})

    response = s.execute()
    responseDict = response.to_dict()
    foundCity = None
    foundOther = None

    nbRes = responseDict['hits']['total']['value']
    if nbRes > 0:
        resContent = responseDict['hits']['hits']
        for i in range(len(resContent)):
            res = resContent[i]['_source']
            fuziness = fuzz.ratio(name, res['name'])

            if res['featureClass'] == 'P':
                if fuziness > 95:
                    if foundCity is None:
                        foundCity = []
                    foundCity.append(res['geonameid'])
            else:
                if fuziness > 65 and res['admin2Code'] is not None:
                    if foundOther is None:
                        foundOther = []
                    foundOther.append(res['geonameid'])

        if foundCity is None:
            return foundOther
        else :
            return foundCity


def searchGeoidByName(name):
    es = Elasticsearch(["https://elastic:abQ4dELdOF6BDjxlotnF8JPW@a6e8c7481efc4507a806032397318270.eu-central-1.aws.cloud.es.io:9243"])
    s = Search(using=es, index="alternatenames-2019.05.17")
    s = s.query("match", alternatename=name)
    s.aggs.bucket('countResults', 'terms', field='geonameid.keyword')

    response = s.execute()
    responseDict = response.to_dict()
    found = None

    results = responseDict['aggregations']['countResults']['buckets']
    if len(results) > 0:
        i = 0
        found = []
        for i in range(len(results)):
            if i == 3:
                break

            geonameId = results[i]['key']
            docCount = results[i]['doc_count']
            if docCount >= 5:
                resultGeoname = searchAllByGeonameid(geonameId)
                if resultGeoname is not None:
                    nameLookup = resultGeoname['name']
                    fuziness = fuzz.ratio(name, nameLookup)
                    if fuziness > 50:
                        found.append(resultGeoname)
    return found

def textProcessing(text):
    text = re.sub(r'\-', ' ', text)
    text = re.sub(r'\"', '', text)
    text = re.sub(r'\.\s*(?=)[A-Z]', lambda m: m.group().lower(), text)  # cute. This is a phrase -> cute. this is..
    text = re.sub('^[A-Z]', lambda m: m.group().lower(), text, flags=re.M)
    placeDict = dict()
    placeRegex = re.compile(r'([A-Z][A-Za-z]+(\s+[A-Z][a-z]+)*)')
    hashtagRegex = re.compile(r'\#[A-Za-z0-9]*')
    places = placeRegex.findall(text)
    hashtags = hashtagRegex.findall(text)

    for place in places:
        place = place[0].strip()
        place = re.sub(r'\bThe\b', '', place)
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

    return placeDict

def analyze(str):
    cityDict = dict()
    countryDict = dict()
    continentDict = dict()
    placeDict = dict()

    resultDict = dict()

    placeExtracted = textProcessing(str)
    if placeExtracted is not None:
        for place in placeExtracted:
            type = None
            resultPlace = []
            placeInfoArray = translateCountry(place)

            if placeInfoArray is not None:
                type = 'Country'
            else:
                type = 'Other'

            if type == 'Country':
                placeObject = Place()
                info = searchAllByGeonameid(placeInfoArray)
                placeObject.name = info['name']
                placeObject.type = info['featureClass']
                if info['countryCode'] is not None:
                    placeObject.ofCountry = info['countryCode']
                else:
                    placeObject.ofCountry = "Not Available"

                if place not in countryDict:
                    countryDict[place] = dict()
                countryDict[place]['count'] = placeExtracted[place]
                countryDict[place]['info'] = placeObject

            if type == 'Other':
                infoArray = None
                placeInfoArray = searchGeoidPlaceByName(place)
                if placeInfoArray is not None:
                    for placeInfo in placeInfoArray:
                        placeObject = Place()
                        info = searchAllByGeonameid(placeInfo)
                        placeObject.name = info['name']
                        placeObject.type = info['featureClass']

                        if info['featureClass'] == 'P':
                            placeObject.ofCountry = info['countryCode']
                            if place not in cityDict:
                                cityDict[place] = dict()
                                cityDict[place]['info'] = []
                            cityDict[place]['info'].append(placeObject)
                            cityDict[place]['count'] = placeExtracted[place]
                        else:
                            placeObject.ofCountry = info['countryCode']
                            placeObject.ofCity = searchCityByCode(
                                info['countryCode'] + "." + info['admin1Code'] + "." + info[
                                    'admin2Code'])
                            if place not in placeDict:
                                placeDict[place] = dict()
                                placeDict[place]['info'] = []
                            placeDict[place]['info'].append(placeObject)
                            placeDict[place]['count'] = placeExtracted[place]

        maxCountCountry = 0
        maxConutryElement = None
        for country in countryDict:
            if countryDict[country]['count'] >= maxCountCountry:
                maxCountCountry = countryDict[country]['count']
                maxConutryElement = [country, countryDict[country]]

        maxCountCity = 0
        maxCityElement = None
        for city in cityDict:
            if cityDict[city]['count'] >= maxCountCity:
                maxCountCity = cityDict[city]['count']
                maxCityElement = [city, cityDict[city]]

        maxCountPlace = 0
        maxPlaceElement = None
        for place in placeDict:
            if placeDict[place]['count'] >= maxCountPlace:
                maxCountPlace = placeDict[place]['count']
                maxPlaceElement = [place, placeDict[place]]

        resultDict['country'] = maxConutryElement
        resultDict['city'] = maxCityElement
        resultDict['place'] = maxPlaceElement


    return resultDict

def showResult(arrayResult):

        if arrayResult['country'] is not None:
            print('Country: {} show {} times in the document'.format(arrayResult['country'][0], arrayResult['country'][1]['count']))
            print('******************\n')

        if arrayResult['city'] is not None:
            arrayInfoCity = ''
            for info in arrayResult['city'][1]['info']:
                arrayInfoCity += 'name: ' + info.name + ', ' + 'country: ' + info.ofCountry + ' || '
            print('City: {} show {} times in the document with informations\n {}'.format(arrayResult['city'][0], arrayResult['city'][1]['count'], arrayInfoCity))
            print('******************\n')

        if arrayResult['place'] is not None:
            arrayInfoPlace = ''
            for info in arrayResult['place'][1]['info']:
                arrayInfoPlace += 'name: ' + info.name + ', ' + 'city: ' + info.ofCity + ', ' + 'country: ' + info.ofCountry + ' || '
            print('Place: {} show {} times in the document with informations\n {}'.format(arrayResult['place'][0],
                                                                                         arrayResult['place'][1]['count'],
                                                                                         arrayInfoPlace))
            print('******************\n')
