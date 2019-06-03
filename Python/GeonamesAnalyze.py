import re
from heapq import nlargest
from Place import *
from GeonamesSearch import *

THRESHOLD_KEYWORD = 2
TOPHITS = 3

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

    stopWordRegexArray = ['\bThe\b', '\bLe\b', '\bLa\b', '\bL\'\b', '\bUn\b', '\bUne\b', \
                     '\bTa\b', '\bTon\b', '\bSon\b', '\bSa\b', '\bSes\b', '\bVotre\b', '\bNotre\b', \
                     '\bJe\b', '\bTu\b', '\bNous\b', '\bVous\b', '\bIl\b', '\bElle\b']
    for place in places:
        place = place[0].strip()
        for stopWordRegex in stopWordRegexArray:
            place = re.sub(stopWordRegex, '', place)
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
    #print(extractedCityCountry)
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
            arrayPlace = searchPlaceByName(placename, dictCityCountry)

            if arrayPlace is not None:
                for item in arrayPlace:
                    placeObject = Place()
                    placeObject.name = item['name']
                    placeObject.ofCountry = item['countryCode']
                    placeObject.ofCity = item['countryCode'] + "." + item['admin1Code'] + "." + item['admin2Code']
                    placeDict[placename] = placeObject
                    placeTopCountDict[placename] = place[1]


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
            for place in topPlace:
                resultDict['place'][place] = [placeTopCountDict[place], placeDict[place]]

    return resultDict

def showStatement(statement, lengthTable):
    print(statement +  ' '*(lengthTable - len(statement) - 1) + '*')

def showResult(arrayResult):
    lengthTable = 58
    if arrayResult['country'] is not None:
        print('**********************************************************')
        print('*                      Pays trouvés                      *')
        print('**********************************************************')
        for country in arrayResult['country']:
            count = arrayResult['country'][country][0]
            info = arrayResult['country'][country][1]
            showStatement('* [{}] apparait {} fois dans le document'.format(country, count), lengthTable)
            showStatement('* [{}] Code Pays: {}'.format(country, info.ofCountry), lengthTable)
        print('**********************************************************')
        print('\n')
    else:
        print('**********************************************************')
        print('*            Pas d\'information pour les pays            *')
        print('**********************************************************')
        print('\n')

    if arrayResult['city'] is not None:
        print('**********************************************************')
        print('*                     Villes trouvés                     *')
        print('**********************************************************')
        for city in arrayResult['city']:
            count = arrayResult['city'][city][0]
            info = arrayResult['city'][city][1]
            showStatement('* [{}] apparait {} fois dans le document'.format(city, count), lengthTable)
            showStatement('* [{}] Code Pays: {}'.format(city, info.ofCountry), lengthTable)
        print('**********************************************************')
        print('\n')
    else:
        print('**********************************************************')
        print('*           Pas d\'information pour les villes           *')
        print('**********************************************************')
        print('\n')


    if arrayResult['place'] is not None:
        print('**********************************************************')
        print('*                     Lieux trouvés                      *')
        print('**********************************************************')
        for place in arrayResult['place']:
            count = arrayResult['place'][place][0]
            info = arrayResult['place'][place][1]
            showStatement('* [{}] apparait {} fois dans le document'.format(place, count), lengthTable)
            showStatement('* [{}] Code Pays: {}'.format(place, info.ofCountry), lengthTable)
            showStatement('* [{}] Villes: {}'.format(place, searchCityByCode(info.ofCity)), lengthTable)
        print('**********************************************************')
        print('\n')
    else :
        print('**********************************************************')
        print('*            Pas d\'information pour les lieux            *')
        print('**********************************************************')
        print('\n')

def analyzeResult(arrayResult):
    print('Pays statistique')
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
            continent = searchContinentByISO(info.ofCountry)
            if prevContinent is None:
                prevContinent = continent
            countryStat[country] = [(arrayResult['country'][country][0]/totalCountCountry*100), continent, info.ofCountry]
            if continent != prevContinent:
                sameContinent = False
            prevContinent = continent

        if sameContinent is True and len:
            print('Les pays ci-dessus se situent dans le meme continent {}'.format(prevContinent))

        for country in countryStat:
            if countryStat[country][0] > 60:
                print('[{}] occupe une partie importante de résultat de {}%'.format(country, countryStat[country][0]))

    print('Villes statistique')
    if arrayResult['city'] is not None:
        for city in arrayResult['city']:
            info = arrayResult['city'][city][1]
            for country in countryStat:
                if info.ofCountry == countryStat[country][2]:
                    print('[{}] appartient à {}'.format(city, country))




















