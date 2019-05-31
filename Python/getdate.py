# -*- coding: utf-8 -*-
import datefinder
import dateparser
from dateutil import parser
from datetime import datetime
from requeteMongo import *


def most_frequent(List):
    counter = 0
    if List:
        num = List[0]
        for i in List:
            curr_frequency = List.count(i)
            if (curr_frequency > counter):
                counter = curr_frequency
                num = i
    if counter == 0:
        num = ""

    return num, counter


def getDate_datefinder(txt):
    matches = datefinder.find_dates(txt)
    list_date = []
    for match in matches:
        if match.year >= 2019:
            list_date.append(match)
    return list_date


def getDate(tweet, tweetDate):
    # str to date 
    tweetDate = parser.parse(tweetDate)

    # str to list of word
    tweet = tweet.lower()
    word_list = tweet.split()

    # static Day, Month, After, befor
    Day = "lundi mardi mercredi jeudi vendredi samedi dimanche"
    Day = Day.split()

    Month = "janvier février mars avril mai juin juillet août septembre octobre novembre décembre"
    Month = Month.split()

    After = "suivant prochain suivante prochaine"
    After = After.split()

    Duree1 = "de partir"
    Duree1 = Duree1.split()

    Duree2 = "à jusqu'à au"
    Duree2 = Duree2.split()

    # search day and Month in the txt
    Day_in_txt = set(word_list).intersection(set(Day))
    Month_in_txt = set(word_list).intersection(set(Month))

    # look for the word befor/after the day
    date_final = []
    for item in Day_in_txt:
        if item in word_list[1:]:
            try:
                if word_list[word_list.index(item) - 1] in After or word_list[word_list.index(item) + 1] in After:
                    date_final.append(datetime.datetime(tweetDate.year, tweetDate.month, tweetDate.day + 7))      
            except:
                pass
    for item in Month_in_txt:
        if item in word_list[1:]:
            try:
                if word_list[word_list.index(item) - 1] in After or word_list[word_list.index(item) + 1] in After:
                    date_final.append(datetime.datetime(tweetDate.year, tweetDate.month + 1, tweetDate.day))
            except:
                pass

    date_final = date_final + getDate_datefinder(tweet)
    # print "*****************date finder*****************"
    # print date_final

    for item in word_list:

        if item == "demain":
            date_final.append(datetime.datetime(tweetDate.year, tweetDate.month, tweetDate.day + 1))
        elif item == "aujourd'hui":
            date_final.append(datetime.datetime(tweetDate.year, tweetDate.month, tweetDate.day))
        elif item == "hier":
            date_final.append(datetime.datetime(tweetDate.year, tweetDate.month, tweetDate.day - 1))

    date_format = []
    for item in date_final:
        date_format.append(item.strftime("%Y-%m-%d %H:%M"))
        # print("date final", item)

    Frequency_Date, counter = most_frequent(date_format)
    # print("nost frequent date", Frequency_Date)
    # print(" number of appearance ", counter)

    # Duration
    listeDuree1 = []
    listeDuree2 = []
    for item in Duree1:
        if item in word_list[1:]:
            try:
                if dateparser.parse(word_list[word_list.index(item) + 1]):
                    try:
                        if word_list[word_list.index(item) + 2] in Duree2:
                            dat1 = dateparser.parse(word_list[word_list.index(item) + 1])
                            dat1 = dat1.strftime("%Y-%m-%d %H:%M")
                            dat2 = dateparser.parse(word_list[word_list.index(item) + 3])
                            dat2 = dat2.strftime("%Y-%m-%d %H:%M")
                            listeDuree1.append()
                            listeDuree2.append()
                    except:
                        pass
            except:
                pass
            

    # compare duration and date
    Frequency_Duration, value_Duration = most_frequent(listeDuree1)
    # print("the ate most frequency durantion in tweets " + str(Frequency_Duration) + " number of appearance " + str(value_Duration))
    
    if value_Duration != 0 and value_Duration >= counter:
        Event_Date = str(Frequency_Duration)
        index = listeDuree1.index(Frequency_Duration)
        Event_Date += " à "
        Event_Date += str(listeDuree2[index])
        duration_bool = True
    elif counter != 0:
        Event_Date = Frequency_Date
        duration_bool = False
    else:
        duration_bool = False
        Event_Date = ""


    return Event_Date, duration_bool


def getDate2(docs):
    tweetDate = []
    tweetDuration = []
    for doc in docs:
        tweet_date, duration = getDate(doc['tweet_text'], doc['created'])
        if duration:
            tweetDuration.append(tweet_date)
        else:
            tweetDate.append(tweet_date)
    tweetDate = [x for x in tweetDate if x != ""]

    Frequency_Date, counter_date = most_frequent(tweetDate)
    if tweetDuration:
        Frequency_Duration, counter_duration = most_frequent(tweetDuration)
    else:
        counter_duration = 0

    if counter_duration >= counter_date and counter_duration != 0:
        return Frequency_Duration
    elif counter_date != 0:
        return Frequency_Date
    else:
        return "We can not get a date for this trend"








