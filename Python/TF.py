import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import math
import textdistance

from spellchecker import SpellChecker

from requeteMongo import searchTextInTitleFluxRSS

spell = SpellChecker(language = 'fr')
TRESHOLD_APPEARENCE = 0.2

#Fonction qui recherche la description des tweets
def tweetDescription(text, nbTweets, docs1):
    # find keywords
    listKeywords = createListKeywords(text, nbTweets)
    result = chooseResult(listKeywords, 10)
    result = deleteSubstr(result)
    result = createResultText(result)
    result = deleteDuplicates(result)
    print(result)

    # find rss article
    print('resultat flux rss : ' + searchTextInTitleFluxRSS(result))

    # find representative tweet
    representativeTweet = selectRepresentativeTweet(result, docs1)
    print('tweet representatif : ' + representativeTweet)
    # setEventDescriptionByTrend(trend, top(list, 1))

    print('***************************')

def deleteDuplicates(text):
    # Seperate out each word
    words = text.split(" ")

    # Convert all words to lowercase
    words = lower(words)

    # Sort the words in order
    words.sort()
    unique = ''
    total_words = len(words)
    i = 0

    while i < (total_words - 1):
        if words[i] != words[i + 1]:
            unique += ' ' + words[i]
        i += 1

    return unique
def deleteSubstr(listKeywords = {}):
    i=0
    listKeywords1=listKeywords.copy()
    for w in list(listKeywords):
        for w1 in list(listKeywords1):
            if (w1 in w) and w!=w1:
                del listKeywords[w1]
                del listKeywords1[w1]
    return listKeywords


def createListKeywords(text, nbTweets):
    list = fiftgrams(text , nbTweets)
    #print(ntop(list, 5))
    #print(top(list))
    lFIFTGRAMS = ntop(list, 5)
    lfiftgrams = top(list)

    list = quadrigrams(text , nbTweets)
    #print(ntop(list, 5))
    #print(top(list))
    lQUADRIGRAMS = ntop(list, 5)
    lquadrigrams = top(list)

    list = trigrams(text , nbTweets)
    #print(ntop(list,5))
    #print(top(list))
    lTRIGRAMS = ntop(list, 5)
    ltrigrams = top(list)

    list = bigrams(text , nbTweets)
    #print(ntop(list,5))
    #print(top(list))
    lBIGRAMS = ntop(list, 5)
    lbigrams = top(list)

    list = TF(text, nbTweets)
    #print(ntop(list,5))
    #print(top(list))
    lTF = ntop(list,5)
    ltf = top(list)

    mylist = []
    for i in lFIFTGRAMS:
        mylist.append([i, lFIFTGRAMS[i]])
    for i in lQUADRIGRAMS:
        mylist.append([i, lQUADRIGRAMS[i]])
    for i in lTRIGRAMS:
        mylist.append([i, lTRIGRAMS[i]])
    for i in lBIGRAMS:
        mylist.append([i, lBIGRAMS[i]])
    for i in lTF:
        mylist.append([i, lTF[i]])

    return mylist

def selectRepresentativeTweet(result, docs):
    max = 0
    representativeTweet = ''
    for doc in docs:
        distance = textdistance.jaccard(result, doc['tweet_text'])
        if distance>max and percentageBadOrthograph(doc['tweet_text'])<0.3:
            max = distance
            representativeTweet = doc['tweet_text']
    return representativeTweet

def percentageBadOrthograph(text):
    words = word_tokenize(text)
    misspelled = spell.unknown(words)
    # print(misspelled)
    count_misspeled = len(misspelled)
    if(nbWords(text)==0):
        return 1
    return count_misspeled/nbWords(text)

def deleteStopWords(words) :
    stopWords = set(stopwords.words('french'))
    myStopWords = ['alors', 'va', 'a', 'au', 'aucuns', 'aussi', 'autre', 'avant', 'avec', 'avoir', 'bon', 'car', 'ce', 'cela', 'ces', 'ceux', 'chaque', 'ci', 'comme', 'comment', 'dans', 'des', 'du', 'dedans', 'dehors', 'depuis', 'devrait', 'doit', 'donc', 'dos', 'début', 'elle', 'elles', 'en', 'encore', 'essai', 'est', 'et', 'eu', 'fait', 'faites', 'fois', 'font', 'hors', 'ici', 'il', 'ils', 'je', 'juste', 'la', 'le', 'les', 'leur', 'là', 'ma', 'maintenant', 'mais', 'mes', 'mine', 'moins', 'mon', 'mot', 'même', 'ni', 'nommés', 'notre', 'nous', 'ou', 'où', 'par', 'parce', 'pas', 'peut', 'peu', 'plupart', 'pour', 'pourquoi', 'quand', 'que', 'quel', 'quelle', 'quelles', 'quels', 'qui', 'sa', 'sans', 'ses', 'seulement', 'si', 'sien', 'son', 'sont', 'sous', 'soyez', 'sujet', 'sur', 'ta', 'tandis', 'tellement', 'tels', 'tes', 'ton', 'tous', 'tout', 'trop', 'très', 'tu', 'voient', 'vont', 'votre', 'vous', 'vu', 'ça', 'étaient', 'état', 'étions', 'été', 'être']
    for word in myStopWords :
        stopWords.add(word)
    tmp = []
    for word in words :
        if word not in stopWords:
            tmp.append(word)
    tmp = [word for word in tmp if (word.isalpha() or word.isnumeric())]
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

def TF(text, nbTweets):
    nb = nbWords(text)
    listWords = countEachWord(text)
    for word in listWords :
        listWords[word]=listWords[word]/nbTweets
    print("This is TF")
    return listWords


def bigrams(text, nbTweets):
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
        listWords[word]=listWords[word]/nbTweets

    print("This is bi-grams")
    return  listWords

def trigrams(text, nbTweets):
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
        listWords[word]=listWords[word]/nbTweets
    print("This is tri-grams")
    return  listWords


def quadrigrams(text, nbTweets):
    words = word_tokenize(text)
    words = lower(words)
    words = deleteStopWords(words)
    i=0
    triwords = []
    listWords = {}
    while i<len(words)-3:
        triwords.append(words[i]+' '+words[i+1]+' '+words[i+2]+' '+words[i+3])
        i+=1

    for word in triwords :
        if word in listWords :
            listWords[word]+=1
        else :
            listWords[word]=1

    for word in listWords :
        listWords[word]=listWords[word]/nbTweets
    print("This is quadri-grams")
    return  listWords

def fiftgrams(text, nbTweets):
    words = word_tokenize(text)
    words = lower(words)
    words = deleteStopWords(words)
    i=0
    triwords = []
    listWords = {}
    while i<len(words)-4:
        triwords.append(words[i]+' '+words[i+1]+' '+words[i+2]+' '+words[i+3]+' '+words[i+4])
        i+=1

    for word in triwords :
        if word in listWords :
            listWords[word]+=1
        else :
            listWords[word]=1

    for word in listWords :
        listWords[word]=listWords[word]/nbTweets
    print("This is fift-grams")
    return  listWords


def sixgrams(text, nbTweets):
    words = word_tokenize(text)
    words = lower(words)
    words = deleteStopWords(words)
    i=0
    triwords = []
    listWords = {}
    while i<len(words)-5:
        triwords.append(words[i]+' '+words[i+1]+' '+words[i+2]+' '+words[i+3]+' '+words[i+4]+' '+words[i+5])
        i+=1

    for word in triwords :
        if word in listWords :
            listWords[word]+=1
        else :
            listWords[word]=1

    for word in listWords :
        listWords[word]=listWords[word]/nbTweets
    print("This is six-grams")
    return  listWords


def sevengrams(text, nbTweets):
    words = word_tokenize(text)
    words = lower(words)
    words = deleteStopWords(words)
    print(len(words))
    i=0
    triwords = []
    listWords = {}
    while i<len(words)-6:
        triwords.append(words[i]+' '+words[i+1]+' '+words[i+2]+' '+words[i+3]+' '+words[i+4]+' '+words[i+5]+' '+words[i+6])
        i+=1

    for word in triwords :
        if word in listWords :
            listWords[word]+=1
        else :
            listWords[word]=1

    for word in listWords :
        listWords[word]=listWords[word]/nbTweets
    print("This is seven-grams")
    return  listWords

def eightgrams(text, nbTweets):
    words = word_tokenize(text)
    words = lower(words)
    words = deleteStopWords(words)
    i=0
    triwords = []
    listWords = {}
    while i<len(words)-7:
        triwords.append(words[i]+' '+words[i+1]+' '+words[i+2]+' '+words[i+3]+' '+words[i+4]+' '+words[i+5]+' '+words[i+6]+' '+words[i+7])
        i+=1

    for word in triwords :
        if word in listWords :
            listWords[word]+=1
        else :
            listWords[word]=1

    for word in listWords :
        listWords[word]=listWords[word]/nbTweets
    print("This is eight-grams")
    return  listWords

def ninegrams(text, nbTweets):
    words = word_tokenize(text)
    words = lower(words)
    words = deleteStopWords(words)
    i=0
    triwords = []
    listWords = {}
    while i<len(words)-8:
        triwords.append(words[i]+' '+words[i+1]+' '+words[i+2]+' '+words[i+3]+' '+words[i+4]+' '+words[i+5]+' '+words[i+6]+' '+words[i+7]+' '+words[i+8])
        i+=1

    for word in triwords :
        if word in listWords :
            listWords[word]+=1
        else :
            listWords[word]=1

    for word in listWords :
        listWords[word]=listWords[word]/nbTweets
    print("This is nine-grams")
    return  listWords

def ntop(listWords,n):
    listWordsMax = []
    max = []
    i=0
    while i < n:
        max.append(0)
        listWordsMax.append('')
        i+=1


    for word in listWords :
        if listWords[word]>TRESHOLD_APPEARENCE :
            i = n - 1;
            while i>=0 :
                if listWords[word]>max[i]:
                    j = 0
                    while j<i:
                        max[j] = max[j+1]
                        listWordsMax[j]=listWordsMax[j+1]
                        j+=1
                    max[i]=listWords[word]
                    listWordsMax[i]=word
                    break
                i-=1

    mylist = {}
    i=0
    while i < len(listWordsMax):
        mylist[listWordsMax[i]]=max[i]
        i+=1
    return mylist


def top(listWords):
    wordMax = ''
    max = 0
    i=0

    for word in listWords :
        if listWords[word]>TRESHOLD_APPEARENCE :
            if listWords[word]>max:
                max=listWords[word]
                wordMax=word
                i-=1
    myreturn = []
    myreturn.append(wordMax)
    myreturn.append(max)

    return myreturn

def chooseResult1(fivegrams, fourgrams, thirdgrams, bigrams,tf, TF):
    coef = 2
    myresult = fivegrams[0]
    if(fivegrams[1]*coef<fourgrams[1]):
        myresult = fourgrams[0]
    if(fourgrams[1]*coef<thirdgrams[1]):
        myresult = thirdgrams[0]
    if(thirdgrams[1]*coef<bigrams[1]):
        myresult = bigrams[0]
    if(bigrams[1]*coef<tf[1]):
        myresult = TF

    return myresult

def chooseResult(listKeywords,n):
    listWordsMax = []
    max = []
    i = 0
    while i < n:
        max.append(0)
        listWordsMax.append('')
        i += 1

    for w in listKeywords:
        if w[1] > TRESHOLD_APPEARENCE:
            i = n - 1;
            while i >= 0:
                if w[1] > max[i]:
                    j = 0
                    while j < i:
                        max[j] = max[j + 1]
                        listWordsMax[j] = listWordsMax[j + 1]
                        j += 1
                    max[i] = w[1]
                    listWordsMax[i] = w[0]
                    break
                i -= 1

    mylist = {}
    i = 0
    while i < len(listWordsMax):
        mylist[listWordsMax[i]] = max[i]
        i += 1
    return mylist


def createResultText(mylist):
    text = ''
    for i in mylist:
        text += ' '+i

    return text


#file = open('./tweets/#19hRuthElkrief.txt','r',encoding='utf-8')
#text = file.read()
#text = "mon text , jd , ! ! ! , , ,$ $"
#file.close()