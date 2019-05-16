import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import math

def deleteStopWords(words) :
    stopWords = set(stopwords.words('french'))
    myStopWords = ['alors', 'va', 'a', 'au', 'aucuns', 'aussi', 'autre', 'avant', 'avec', 'avoir', 'bon', 'car', 'ce', 'cela', 'ces', 'ceux', 'chaque', 'ci', 'comme', 'comment', 'dans', 'des', 'du', 'dedans', 'dehors', 'depuis', 'devrait', 'doit', 'donc', 'dos', 'début', 'elle', 'elles', 'en', 'encore', 'essai', 'est', 'et', 'eu', 'fait', 'faites', 'fois', 'font', 'hors', 'ici', 'il', 'ils', 'je', 'juste', 'la', 'le', 'les', 'leur', 'là', 'ma', 'maintenant', 'mais', 'mes', 'mine', 'moins', 'mon', 'mot', 'même', 'ni', 'nommés', 'notre', 'nous', 'ou', 'où', 'par', 'parce', 'pas', 'peut', 'peu', 'plupart', 'pour', 'pourquoi', 'quand', 'que', 'quel', 'quelle', 'quelles', 'quels', 'qui', 'sa', 'sans', 'ses', 'seulement', 'si', 'sien', 'son', 'sont', 'sous', 'soyez', 'sujet', 'sur', 'ta', 'tandis', 'tellement', 'tels', 'tes', 'ton', 'tous', 'tout', 'trop', 'très', 'tu', 'voient', 'vont', 'votre', 'vous', 'vu', 'ça', 'étaient', 'état', 'étions', 'été', 'être']
    for word in myStopWords :
        stopWords.add(word)
    tmp = []
    for word in words :
        if word not in stopWords:
            tmp.append(word)
    tmp = [word for word in tmp if word.isalpha()]
    return tmp

def lower(words):
    i=0
    tmp = []
    while i < len(words) :
        tmp.append(words[i].lower())
        i+=1
    return tmp

def nbWords(text):
    count = 0
    words = word_tokenize(text)
    words = deleteStopWords(words)
    for word in words :
        count +=1
    return count

def countEachWord(text):
    listWords = {}
    words = word_tokenize(text)
    words = lower(words)
    words = deleteStopWords(words)
    for word in words :
        if word in listWords :
            listWords[word]+=1
        else :
            listWords[word]=1
    return listWords

def TF(text):
    nb = nbWords(text)
    listWords = countEachWord(text)
    for word in listWords :
        listWords[word]=listWords[word]/nb
    print("This is TF")
    return listWords


def bigrams(text):
    words = word_tokenize(text)
    words = lower(words)
    words = deleteStopWords(words)
    i=0
    biwords = []
    listWords = {}
    while i<len(words)-1:
        biwords.append(words[i]+' '+words[i+1])
        i+=1

    for word in biwords :
        if word in listWords :
            listWords[word]+=1
        else :
            listWords[word]=1

    for word in listWords :
        listWords[word]=listWords[word]/i

    print("This is bi-grams")
    return  listWords

def trigrams(text):
    words = word_tokenize(text)
    words = lower(words)
    words = deleteStopWords(words)
    i=0
    triwords = []
    listWords = {}
    while i<len(words)-2:
        triwords.append(words[i]+' '+words[i+1]+' '+words[i+2])
        i+=1

    for word in triwords :
        if word in listWords :
            listWords[word]+=1
        else :
            listWords[word]=1

    for word in listWords :
        listWords[word]=listWords[word]/i
    print("This is tri-grams")
    return  listWords

def top(listWords,n):
    listWordsMax = []
    max = []
    i=0
    while i < n:
        max.append(0)
        listWordsMax.append('')
        i+=1


    for word in listWords :
        i = n - 1;
        while i>=0 :
            if listWords[word]>max[i]:
                max[i]=listWords[word]
                listWordsMax[i]=word
                break
            i-=1
    return listWordsMax




file = open('./tweets/#19hRuthElkrief.txt','r',encoding='utf-8')
text = file.read()
#text = "mon text , jd , ! ! ! , , ,$ $"
list = trigrams(text)
print(top(list,5))

list = bigrams(text)
print(top(list,5))

list = TF(text)
print(top(list,5))


file.close()