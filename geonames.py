import requests
import re
from fuzzywuzzy import fuzz
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from Place import *
from elasticsearch_dsl import connections


def searchGeoidCountryByName(name):
    es = Elasticsearch(
        ["https://elastic:abQ4dELdOF6BDjxlotnF8JPW@a6e8c7481efc4507a806032397318270.eu-central-1.aws.cloud.es.io:9243"])
    s = Search(using=es, index="countryinfo-2019.05.27")
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
        else:
            return None
    else:
        return None

def searchAllByGeonameid(geonameid):
    es = Elasticsearch(
        ["https://elastic:abQ4dELdOF6BDjxlotnF8JPW@a6e8c7481efc4507a806032397318270.eu-central-1.aws.cloud.es.io:9243"])
    s = Search(using=es, index="geoname-2019.05.16")
    s = s.query("match", geonameid=geonameid)

    response = s.execute()
    responseDict = response.to_dict()
    found = None

    nbRes = responseDict['hits']['total']['value']
    if nbRes > 0:
        found = responseDict['hits']['hits'][0]['_source']
    return found


def searchGeoidPlaceByName(name):
    es = Elasticsearch(
        ["https://elastic:abQ4dELdOF6BDjxlotnF8JPW@a6e8c7481efc4507a806032397318270.eu-central-1.aws.cloud.es.io:9243"])
    s = Search(using=es, index="geoname-2019.05.16")
    s = s.query("match", name=name)
    s = s.query("exists", field="alternatenames")
    #s = s.sort({"_script": {
    #     "script": "doc['alternatenames.keyword'].size()",
    #     "type": "number",
    #     "order": "asc"
    #  }
   #})

    response = s.execute()
    responseDict = response.to_dict()
    found = None

    nbRes = responseDict['hits']['total']['value']
    if nbRes > 0:
        found = []
        resContent = responseDict['hits']['hits']
        for i in range(len(resContent)):
            if len(found) == 5:
                break
            res = resContent[i]['_source']
            fuziness = fuzz.ratio(name, res['name'])
            if fuziness > 65:
                found.append(res['geonameid'])

    return found


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
    placeDict = []
    placeRegex = re.compile(r'([A-Z][A-Za-z]+(\s+[A-Z][a-z]+)*)')
    hashtagRegex = re.compile(r'\#[A-Za-z0-9]*')
    places = placeRegex.findall(text)
    hashtags = hashtagRegex.findall(text)

    for place in places:
        place = place[0].strip()
        placeDict.append(place)

    for hashtag in hashtags:
        hashtag = hashtag.replace('#', '')
        if re.search('^[a-z].*', hashtag):
            hashtag = hashtag.capitalize()  # notredame -> Notredame

        placeDict.append(hashtag)

    for place in placeDict:
        if place.isupper():  # WASHINGTON -> #Washington
            place = place.lower()
            place = place.capitalize()

        placeSplit = place.split()
        if len(placeSplit) > 0:
            for i in range(len(placeSplit)):
                upperCaseWord = re.findall('[A-Z][^A-Z]*', placeSplit[i])  # NotreDame -> Notre Dame
                if len(upperCaseWord) > 1:
                    placeSplit[i] = " ".join(upperCaseWord)
            place = " ".join(placeSplit)

    return placeDict

if __name__ == '__main__':
    #str = "Today i visited Paris, they have an amazing cathedral named Notre-Dame"
    f = open("/Users/phucvu/Desktop/elastic/logstash-7.0.1/textFile/testText.txt", "r")
    str = f.read()

    placeExtracted = textProcessing(str)
    if placeExtracted is not None:
        for place in placeExtracted:
            type = None
            resultPlace = []
            placeInfoArray = searchGeoidCountryByName(place)

            if placeInfoArray is not None:
                type = 'Country'
            else :
                type = 'Other'

            if type == 'Country' :
                placeObject = Place()
                info = searchAllByGeonameid(placeInfoArray)
                placeObject.name = info['name']
                placeObject.type = info['featureClass']
                if info['countryCode'] is not None:
                    placeObject.ofCountry = info['countryCode']
                else:
                    placeObject.ofCountry = "Not Available"
                resultPlace.append(placeObject)

            if type == 'Other':
                placeInfoArray = searchGeoidPlaceByName(place)
                if placeInfoArray is not None:

                    for placeInfo in placeInfoArray:
                        placeObject = Place()
                        info = searchAllByGeonameid(placeInfo)
                        placeObject.name = info['name']
                        placeObject.type = info['featureClass']
                        if info['countryCode'] is not None:
                            placeObject.ofCountry = info['countryCode']
                        else :
                            placeObject.ofCountry = "Not Available"
                        resultPlace.append(placeObject)

            resultsStr = []
            for element in resultPlace:
                resultsStr.append(
                    '[' + 'name: ' + element.name + ', type: ' + element.type + ', countryCode: ' + element.ofCountry + ']')

            outStr = " || ".join(resultsStr)
            print('<' + place + '>' + outStr)














