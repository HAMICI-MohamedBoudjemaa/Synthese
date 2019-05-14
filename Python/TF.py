import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import math

def deleteStopWords(words) :
    stopWords = set(stopwords.words('french'))
    tmp = []
    for word in words :
        if word not in stopWords:
            tmp.append(word)
    tmp = [word for word in tmp if word.isalpha()]
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
    return listWords


def bigrams(text):
    words = word_tokenize(text)
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


file = open('germinal.txt','r')
text = file.read()
#text = "mon text , jd , ! ! ! , , ,$ $"

list = bigrams(text)

print(top(list,3))

list = TF(text)
print(top(list,3))
file.close()