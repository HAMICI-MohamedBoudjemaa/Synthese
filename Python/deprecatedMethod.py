def searchGeoidCountryByName(name):
    res = None
    #if len(name) == 2 and name.isupper():
    #    res = searchGeoidCountryByISO(name)

    if res is None:
        es = Elasticsearch(
            ["https://elastic:ZsCkeJa6qrPR6YICH8nwCRZR@487a3c18579448be987a324822344a49.eu-central-1.aws.cloud.es.io:9243"])
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

def searchGeoidPlaceByName(name):
    es = Elasticsearch(
        ["https://elastic:ZsCkeJa6qrPR6YICH8nwCRZR@487a3c18579448be987a324822344a49.eu-central-1.aws.cloud.es.io:9243"])
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
    es = Elasticsearch(["https://elastic:ZsCkeJa6qrPR6YICH8nwCRZR@487a3c18579448be987a324822344a49.eu-central-1.aws.cloud.es.io:9243"])
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


def searchGeoidCountryByISO(iso):
    es = Elasticsearch(
        ["https://elastic:ZsCkeJa6qrPR6YICH8nwCRZR@487a3c18579448be987a324822344a49.eu-central-1.aws.cloud.es.io:9243"])
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
        ["https://elastic:ZsCkeJa6qrPR6YICH8nwCRZR@487a3c18579448be987a324822344a49.eu-central-1.aws.cloud.es.io:9243"])
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

def translateCountry(name):
    res = None
    #if len(name) == 2 and name.isupper():
    #    res = searchGeoidCountryByISO(name)
    if res is None:
        es = Elasticsearch(
            ["https://elastic:ZsCkeJa6qrPR6YICH8nwCRZR@487a3c18579448be987a324822344a49.eu-central-1.aws.cloud.es.io:9243"])
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