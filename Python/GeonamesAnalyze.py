import re
from heapq import nlargest
from Python.Place import *
from Python.GeonamesSearch import *
import time
from Python.requeteMongo import *

THRESHOLD_KEYWORD = 3
TOPHITS = 3

def textProcessing(text):
    text = re.sub(r'\-', ' ', text)
    text = re.sub(r'\"', '', text)
    #text = re.sub(r'\.\s*(?=)[A-Z]', lambda m: m.group().lower(), text)  # cute. This is a phrase -> cute. this is..
    #text = re.sub(r'\?\s*(?=)[A-Z]', lambda m: m.group().lower(), text)  # cute? This is a phrase -> cute. this is..
    #text = re.sub(r'\!\s*(?=)[A-Z]', lambda m: m.group().lower(), text)  # cute? This is a phrase -> cute. this is..
    #text = re.sub(r'\:\s*(?=)[A-Z]', lambda m: m.group().lower(), text)  # cute? This is a phrase -> cute. this is..
    #text = re.sub(r'\;\s*(?=)[A-Z]', lambda m: m.group().lower(), text)  # cute? This is a phrase -> cute. this is..
    #text = re.sub(r'\W\s*(?=)[A-Z]', lambda m: m.group().lower(), text)  # cute! This is a phrase -> cute. this is..
    #text = re.sub('^\s*[A-Z]', lambda m: m.group().lower(), text, flags=re.M)
    placeDict = dict()
    placeRegex = re.compile(r'([A-Z][A-Za-zàéèêëîïôûüÿù]+(\s+[A-Z][a-zàéèêëîïôûüÿù]+)*)', re.UNICODE)
    hashtagRegex = re.compile(r'\#[a-zàéèêëîïôûüÿù0-9]+', re.UNICODE)
    places = placeRegex.findall(text)
    hashtags = hashtagRegex.findall(text)

    stopWordArray = ['The', 'Le', 'La', 'L\'', 'Les', 'Un', 'Une', \
                     'Ta', 'Ton', 'Son', 'Sa', 'Ses', 'Votre', 'Notre', \
                     'Je', 'Tu', 'Nous', 'Vous', 'Il', 'Elle', 'Tout', 'Toute',\
                     'Tous', 'Toutes']
    for place in places:
        place = place[0].strip()
        #for stopWordRegex in stopWordRegexArray:
        #    place = re.sub(stopWordRegex, '', place)
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
        if hashtag.isupper():  # WASHINGTON -> Washington
            hashtag = hashtag.lower()
            hashtag = hashtag.capitalize()
        hashtag = hashtag.strip()
        if re.search('^[a-zàéèêëîïôûüÿù].*', hashtag):
            hashtag = hashtag.capitalize()  # notredame -> Notredame

        if hashtag in placeDict:
            placeDict[hashtag] += 1
        else:
            placeDict[hashtag] = 1

    newPlaceDict = dict()
    for key,value in placeDict.items():
        if value > THRESHOLD_KEYWORD and key not in stopWordArray:
            newPlaceDict[key] = value
    placeDict = newPlaceDict
    del(newPlaceDict)
    print('Nombre total d\'occurrence: {}'.format(sum(placeDict.values())))
    print('Nombre total de lieux trouvés: {}'.format(len(placeDict)))
    print(placeDict)
    return placeDict

def analyze(str):
    start_time = time.time()
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
    print("--- Le traitement du text prend %s secondes ---" % (time.time() - start_time))
    extractedPlace = []
    dictCityCountry = dict()
    dictCityCountry['country'] = None
    dictCityCountry['city'] = None

    if extractedCityCountry is not None:
        countryTopCountDict = dict()
        cityTopCountDict = dict()
        placeTopCountDict = dict()
        for extractedItem in extractedCityCountry:
            arrayCityCountry = searchCountryCityByName(extractedItem)
            if arrayCityCountry is not None:
                if arrayCityCountry[0]['featureClass'] == 'A':
                    type = 'Country'
                elif arrayCityCountry[0]['featureClass'] == 'P':
                    type = 'City'

                if type == 'Country':
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
            #print(placename)
            arrayPlace = searchPlaceByName(placename, dictCityCountry)
            #print(arrayPlace)

            if arrayPlace is not None:
                for item in arrayPlace:
                    placeObject = Place()
                    placeObject.name = item['name']
                    placeObject.ofCountry = item['countryCode']
                    placeObject.ofCity = item['countryCode'] + "." + item['admin1Code'] + "." + item['admin2Code']
                    placeDict[placename] = placeObject
                    placeTopCountDict[placename] = place[1]


        if countryTopCountDict :
            topCountry = nlargest(TOPHITS, countryTopCountDict, countryTopCountDict.get)
            resultDict['country'] = dict()
            for country in topCountry:
                resultDict['country'][country] = [countryTopCountDict[country], countryDict[country]]
        if cityTopCountDict:
            topCity = nlargest(TOPHITS, cityTopCountDict, cityTopCountDict.get)
            resultDict['city'] = dict()
            for city in topCity:
                resultDict['city'][city] = [cityTopCountDict[city], cityDict[city]]
        if placeTopCountDict:
            topPlace = nlargest(TOPHITS, placeTopCountDict, placeTopCountDict.get)
            resultDict['place'] = dict()
            for place in topPlace:
                resultDict['place'][place] = [placeTopCountDict[place], placeDict[place]]
        print("--- La recherche de lieux prend %s secondes ---" % (time.time() - start_time))
    return resultDict

def showStatement(statement, lengthTable):
    print(statement +  ' '*(lengthTable - len(statement) - 1) + '*')

def showResult(arrayResult):
    lengthTable = 70
    if arrayResult['country'] is not None:
        print('**********************************************************************')
        print('*                            Pays trouvés                            *')
        print('**********************************************************************')
        for country in arrayResult['country']:
            count = arrayResult['country'][country][0]
            info = arrayResult['country'][country][1]
            showStatement('* [{}] apparait {} fois dans le document, code de pays: {}'.format(country, count, info.ofCountry), lengthTable)
            #showStatement('* [{}] Code Pays: {}'.format(country, info.ofCountry), lengthTable)
        print('**********************************************************************')
        print('\n')
    else:
        print('**********************************************************************')
        print('*                  Pas d\'information pour les pays                  *')
        print('**********************************************************************')
        print('\n')

    if arrayResult['city'] is not None:
        print('**********************************************************************')
        print('*                           Villes trouvés                           *')
        print('**********************************************************************')
        for city in arrayResult['city']:
            count = arrayResult['city'][city][0]
            info = arrayResult['city'][city][1]
            showStatement('* [{}] apparait {} fois dans le document, code de pays: {}'.format(city, count, info.ofCountry), lengthTable)
            #showStatement('* [{}] Code Pays: {}'.format(city, info.ofCountry), lengthTable)
        print('**********************************************************************')
        print('\n')
    else:
        print('**********************************************************************')
        print('*                 Pas d\'information pour les villes                 *')
        print('**********************************************************************')
        print('\n')


    if arrayResult['place'] is not None:
        print('**********************************************************************')
        print('*                           Places trouvés                           *')
        print('**********************************************************************')
        for place in arrayResult['place']:
            count = arrayResult['place'][place][0]
            info = arrayResult['place'][place][1]
            showStatement('* [{}] apparait {} fois dans le document'.format(place, count), lengthTable)
            showStatement('* [{}] Code Pays: {}'.format(place, info.ofCountry), lengthTable)
            showStatement('* [{}] Villes: {}'.format(place, searchCityByCode(info.ofCity)), lengthTable)
        print('**********************************************************************')
        print('\n')
    else :
        print('**********************************************************************')
        print('*                 Pas d\'information pour les lieux                  *')
        print('**********************************************************************')
        print('\n')

def analyzeResult(arrayResult):
    relationalDict = dict()
    # print('Pays statistique')
    countryStat = None
    if arrayResult['country'] is not None:
        countryStat = dict()
        totalCountCountry = 0
        sameContinent = True
        for country in arrayResult['country']:
            totalCountCountry += arrayResult['country'][country][0]

        prevContinent = None
        for country in arrayResult['country']:
            info = arrayResult['country'][country][1]
            continentBelong = searchContinentByISO(info.ofCountry)
            if prevContinent is None:
                prevContinent = continentBelong
            countryStat[country] = [(arrayResult['country'][country][0]/totalCountCountry*100), continentBelong, info.ofCountry]
            if continentBelong != prevContinent:
                sameContinent = False
            prevContinent = continentBelong

        # if countryStat:
        #     if sameContinent is True and len(countryStat) > 1:
        #         print('Les pays ci-dessus se situent dans le meme continent {}'.format(prevContinent))

            # for country in countryStat:
            #     if countryStat[country][0] > 60:
            #         print('Le pays [{}] occupe une partie importante de résultat de {}%'.format(country, countryStat[country][0]))

    print('Villes statistique')
    if arrayResult['city'] is not None:
        cityStat = dict()
        totalCountCity = 0
        sameCountry = True
        print('**********************************************************************')
        print('*                         Villes statistique                         *')
        print('**********************************************************************')
        for city in arrayResult['city']:
            totalCountCity += arrayResult['city'][city][0]

        prevCountry = None
        for city in arrayResult['city']:
            info = arrayResult['city'][city][1]
            countryBelong = info.ofCountry

            if prevCountry is None:
                prevCountry = countryBelong
            cityStat[city] = [(arrayResult['city'][city][0]/totalCountCity*100), countryBelong, info.ofCountry]
            if countryBelong != prevCountry:
                sameCountry = False
            prevCountry = countryBelong


            if countryStat:
                for country in countryStat:
                    if info.ofCountry == countryStat[country][2]:
                        relationalDict[city] = [country]
                        showStatement('[{}] appartient à {}, occupe {}% de résultat trouvé'.format(city, country, round(cityStat[city][0]),2), 70)
                    else:
                        showStatement('[{}] occupe {}% de résultat trouvé'.format(city, round(cityStat[city][0]), 2), 70)
                        #print('La ville [{}] occupe une partie de {}% de résultat trouvé'.format(city, cityStat[city][0]))
        print('**********************************************************************')


        # if cityStat:
        #     if sameCountry is True and len(cityStat) > 1:
        #         print('Les villes ci-dessus se situent dans le meme pays {}'.format(prevCountry))
        #
        #     for city in cityStat:
        #         if cityStat[city][0] > 60:
        #             print('La ville [{}] occupe une partie importante de résultat de {}%'.format(city,
        #                                                                                 cityStat[city][0]))

def writeResult(arrayResult):
    arrayReturn = []
    if arrayResult['country'] is not None:
        for country in arrayResult['country']:
            arrayReturn.append(country)

    if arrayResult['city'] is not None:
        for city in arrayResult['city']:
            arrayReturn.append(city)

    return arrayReturn



















