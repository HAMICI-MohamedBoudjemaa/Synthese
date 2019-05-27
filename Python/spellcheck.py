from spellchecker import SpellChecker
import re
from requeteMongo import getTweetByTrend
from requeteMongo import getAllTrend

def getWords(text):
    return re.compile('\w+').findall(text)

def getStats(trend):
    spell = SpellChecker('fr')
    tweets = ""
    somme = 0
    count = 0
    for doc in getTweetByTrend(trend):
        txt = (doc['tweet_text'])
        #print(txt)
        tweets = tweets + txt
        somme = somme + len(txt)
        count = count + 1
    moyenne = somme / count

    words = getWords(tweets)
    #print(words)
    count_words = len(words)
    print("count words")
    print(count_words)
    print("count tweets")
    print(count)
    misspelled = spell.unknown(words)
    #print(misspelled)
    count_misspeled = len(misspelled)
    print("proportion misspeled")
    print((count_misspeled/count_words)*100)
    print("moyenne longueur tweet")
    print(moyenne)
    print("\n")

trends = getAllTrend()
for t in trends:
    print (t)
    getStats(t)


# f = open("#AvecBardella.txt", "r")
# tweets = f.read()


# find those words that may be misspelled
#
# misspelled = spell.unknown(['l\'artiste', 'trier', 'considerent', 'exiga'])
# for word in misspelled:
#     print(word)
#     # Get the one `most likely` answer
#     print(spell.correction(word))
#     if(spell.correction(word) is None):
#         print("bien orthographié")
#     # Get a list of `likely` options
#     print(spell.candidates(word))