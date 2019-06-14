import re

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

from Python.connexionMongoAtlas import fluxRSS

p_stemmer = nltk.SnowballStemmer('french')
TRESHOLD_SCORE = 1.90

def concatTitleAndDescriptionFluxRSS():
    fluxR = []
    stopWords = set(stopwords.words('french'))
    myStopWords = ['alors', 'va', 'a', 'au', 'aucuns', 'aussi', 'autre', 'avant', 'avec', 'avoir', 'bon', 'car', 'ce',
                   'cela', 'ces', 'ceux',
                   'chaque', 'ci', 'comme', 'comment', 'dans', 'des', 'du', 'dedans', 'dehors', 'depuis', 'devrait',
                   'doit', 'donc', 'dos',
                   'début', 'elle', 'elles', 'en', 'encore', 'essai', 'est', 'et', 'eu', 'fait', 'faites', 'fois',
                   'font', 'hors', 'ici',
                   'il', 'ils', 'je', 'juste', 'la', 'le', 'les', 'leur', 'là', 'ma', 'maintenant', 'mais', 'mes',
                   'mine', 'moins', 'mon',
                   'mot', 'même', 'ni', 'nommés', 'notre', 'nous', 'ou', 'où', 'par', 'parce', 'pas', 'peut', 'peu',
                   'plupart', 'pour',
                   'pourquoi', 'quand', 'que', 'quel', 'quelle', 'quelles', 'quels', 'qui', 'sa', 'sans', 'ses',
                   'seulement', 'si', 'sien',
                   'son', 'sont', 'sous', 'soyez', 'sujet', 'sur', 'ta', 'tandis', 'tellement', 'tels', 'tes', 'ton',
                   'tous', 'tout', 'trop',
                   'très', 'tu', 'voient', 'vont', 'votre', 'vous', 'vu', 'ça', 'étaient', 'état', 'étions', 'été',
                   'être', '-', '«', '»', ',', ';', '.'
                   ':'
                   ]
    for word in myStopWords:
        stopWords.add(word)
    fluxRss = fluxRSS.find()
    res = []
    for flux in fluxRss:
        fluxR = []
        concatString = flux['titre'] + ' ' + flux['description']
        concatString = re.sub(r'[^a-za-zàéèêëîïôûüÿùA-Z\s\d]', '', concatString)
        for i in word_tokenize(concatString):
            if i not in stopWords:
                sstemmed_tokens = p_stemmer.stem(i)
                fluxR.append(sstemmed_tokens)
            fluxrss = " ".join(fluxR)
            # req = tweets.update({}, {'$set': {'fluxRSS': ''}})
        update = fluxRSS.update({'_id':flux['_id']}, {'$set': {'flux_stemm': fluxrss, 'status':True}})
    return update

def addFieldCollectionFluxRSS():
    #req = tweets.update({}, {'$set': {'fluxRSS': ''}})
    for doc in fluxRSS.find():
        fluxRSS.update(
            {'_id': doc['_id']},
            {'$set': {'flux_stemm': '', 'status':False}}, upsert=False, multi=False)


def searchTextInTitleFluxRSS(search_text):
    array = []
    cursor = fluxRSS.find(
        {'$text': {'$search': search_text, "$language": "french", "$diacriticSensitive": True}},
        {'score': {'$meta': 'textScore'}}
    )
    # Sort by 'score' field.
    cursor.sort([('score', {'$meta': 'textScore'})])
    for doc in cursor:
        if TRESHOLD_SCORE < doc['score']:
            array.append(doc)
        #print(doc)
    if not array:
        return ''
    else:
        print('Description : ' + array[0]['description'])
        print('flux stemmer : ' + array[0]['flux_stemm'])
        print('Score : ' + str(array[0]['score']))
        return array[0]['titre']


if __name__ == '__main__':
    print(searchTextInTitleFluxRSS(" 000 10 fiert lill march person pres presqu pridemonth"))

    #concatTitleAndDescriptionFluxRSS()
    # Pour mettre des index

    #fluxRSS.create_index([("flux_stemm", pymongo.TEXT)], default_language='french')
    #fluxRSS.create_index([('flux_stemm', pymongo.TEXT)], name='search_index', default_language='french')

    #addFieldCollectionFluxRSS()