# -*- coding: utf-8 -*-
import datefinder
import dateparser
from datetime import datetime
from datetime import timedelta  

def getDate_datefinder(txt):
    matches = datefinder.find_dates(txt)
    list_date=[]
    for match in matches:
        list_date.append(match)
    return list_date

def getDate(txt):
    # str to list of word
    f = txt.lower()
    word_list = f.split()
    
    #static Day, Month, After, befor
    Day = "lundi mardi mercredi jeudi vendredi samedi dimanche"
    Day = Day.split()

    Month = "janvier février mars avril mai juin juillet août septembre octobre novembre décembre"
    Month = Month.split()

    After = "suivant prochain suivante prochaine"
    After = After.split()

    Duree1 = "de "
    Duree1 = After.split()

    Duree2 = "à"
    Duree2 = After.split()

    #search day and Month in the txt
    Day_in_txt=set(word_list).intersection( set(Day) )
    Month_in_txt=set(word_list).intersection( set(Month) )

    #look for the word befor/after the day
    now = datetime.now()
    date_day = []
    date_Month = []
    for item in Day_in_txt:
        if item in word_list[1:]:
            if word_list[word_list.index(item)-1] in After:
                date_day.append(now.day + 7)
            if word_list[word_list.index(item)+1] in After:
                date_day.append(now.day + 7)
    for item in Month_in_txt:
        if item in word_list[1:]:
            if word_list[word_list.index(item)-1] in After:
                date_Month.append(now.month +1)
            if word_list[word_list.index(item)+1] in After:
                date_Month.append(now.month +1)
    
    #collect all dates
    date_final = []
    for item in date_day:
        date_final.append(datetime(now.year, now.month, item))
    # print "*****************DAY*****************"
    # print date_final

    for item in date_Month:
        date_final.append(datetime(now.year, item, now.day))
    # print "*****************Month*****************"
    # print date_final

    date_final = date_final + getDate_datefinder(txt)
    # print "*****************date finder*****************"
    # print date_final

    # for date_string in word_list:
    #     if dateparser.parse(date_string):
    #         print date_string
    #         date_final.append(dateparser.parse(date_string).date())
    # print "*****************date parser*****************"
    # print date_final

    # Remove old date
    # for item in date_final:
    #     if item < now:
    #         date_final.remove(item)

    # Remove duplicates in the list
    list(set(date_final))

    # Duration
    listeDuree1 = []
    listeDuree2 = []
    for item in Duree1:
        if item in word_list[1:]:
            if dateparser.parse(word_list[word_list.index(item)+1]):
                if word_list[word_list.index(item)+2] in Duree2:
                    listeDuree1.append(dateparser.parse(word_list[word_list.index(item)+1]))
                    listeDuree2.append(dateparser.parse(word_list[word_list.index(item)+3]))
                


    return date_final

if __name__ == '__main__':

    # f = open(r"tweets/#19hRuthElkrief.txt","r")
    # f = f.read()
    # date = getDate(f)
    # print date[7]
    date_string = "vo/co/cccc"
    # if dateparser.parse(date_string):
    #     print date_string
    # else:
    #     print "walo"
    # txt = "lahcen ait bella mcha yl3ab w de zfzf à 09/09/2019 jeudi daro katfo idan howa kasoul jibad"
    # f = txt.lower()
    # word_list = f.split()
    # Day = "lundi mardi mercredi jeudi vendredi samedi dimanche"
    # Day = Day.split()
    # Day_in_txt=set(word_list).intersection( set(Day) )
    # now = datetime.now()
    # Duree1 = "de "
    # Duree1 = Duree1.split()

    # Duree2 = "à"
    # Duree2 = Duree2.split()

    # for item in Duree1:
    #     if item in word_list[1:]:
    #         if dateparser.parse(word_list[word_list.index(item)+1]):
    #             if word_list[word_list.index(item)+2] in Duree2:

    liste = [2,65,42,53,27,2,42,27,2,53,53,53,65,21,27,53,2,53,65,27]
    compte = {}.fromkeys(set(liste),0)
    for valeur in liste:
        compte[valeur] += 1
    key, value = compte.popitem()

    print(key)
                    
    
    


