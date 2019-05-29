# -*- coding: utf-8 -*-
import datefinder
import dateparser
from datetime import datetime
from datetime import timedelta  

global now 
now = datetime.now()

def most_frequent(List): 
    counter = 0
    if List:
        num = List[0] 
        for i in List: 
            curr_frequency = List.count(i) 
            if(curr_frequency > counter): 
                counter = curr_frequency 
                num = i 
    if counter == 0:
        num = ""
  
    return num, counter  

def getDate_datefinder(txt):
    matches = datefinder.find_dates(txt)
    list_date=[]
    for match in matches:
        # print "date finder", match
        if match.year <= 2019:
            list_date.append(datetime(now.year, match.month, match.day))
        else:
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

    Duree1 = "de partir"
    Duree1 = Duree1.split()

    Duree2 = "à jusqu'à au"
    Duree2 = Duree2.split()

    #search day and Month in the txt
    Day_in_txt=set(word_list).intersection( set(Day) )
    Month_in_txt=set(word_list).intersection( set(Month) )

    #look for the word befor/after the day
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
        # print "day", date_day
        date_final.append(datetime(now.year, now.month, item))
    # print "*****************DAY*****************"
    # print date_final

    for item in date_Month:
        # print "month", item
        date_final.append(datetime(now.year, item, now.day))
    # print "*****************Month*****************"
    # print date_final

    date_final = date_final + getDate_datefinder(txt)
    # print "*****************date finder*****************"
    # print date_final

    for item in word_list:
        # if dateparser.parse(item):
        #     date_final.append(dateparser.parse(item).date())
        #     print item
        #     print "date perser", dateparser.parse(item).date()
        if item == "demain":
            date_final.append(datetime(now.year, now.month, now.day + 1))
        elif item == "aujourd'hui":
            date_final.append(datetime(now.year, now.month, now.day))
        elif item == "hier":
            date_final.append(datetime(now.year, now.month, now.day - 1))

    # Remove old date
    # for item in date_final:
    #     if item < now:
    #         date_final.remove(item)
    date_format = []
    for item in date_final:
        date_format.append(item.strftime("%Y-%m-%d %H:%M"))
        print "date final", item

    # get date most frequency         
    # Date_count = {}.fromkeys(set(date_format),0)
    # for item in date_format:
    #     Date_count[item] += 1
    # Frequency_Date, value_Date = Date_count.popitem()
    # print "the ate most frequency date in tweets ", Frequency_Date
    # print " number of appearance ", value_Date
    Frequency_Date, counter = most_frequent(date_format)
    print "nost frequent date", Frequency_Date
    print " number of appearance ", counter

    # Duration
    listeDuree1 = []
    listeDuree2 = []
    for item in Duree1:
        if item in word_list[1:]:
            if dateparser.parse(word_list[word_list.index(item)+1]):
                if word_list[word_list.index(item)+2] in Duree2:
                    listeDuree1.append(dateparser.parse(word_list[word_list.index(item)+1]))
                    listeDuree2.append(dateparser.parse(word_list[word_list.index(item)+3]))

    # compare duration and date
    Frequency_Duration, value_Duration = most_frequent(listeDuree1)

    print "the ate most frequency durantion in tweets " +str(Frequency_Duration)+ " number of appearance " +str(value_Duration)

    if value_Duration >= counter:
        Event_Date = str(Frequency_Duration.strftime("%Y-%m-%d %H:%M"))
        index = listeDuree1.index(Frequency_Duration)
        Event_Date += " à "
        Event_Date += str(listeDuree2[index].strftime("%Y-%m-%d %H:%M"))
    else:
        Event_Date = Frequency_Date


    return Event_Date

if __name__ == '__main__':

    f = open(r"tweets/#AvecBardella.txt","r")
    f = f.read()
    # f = "on aura des tests à faire de demain à 12/01/2020 et juste aujourd'hui on aura rien"
    date = getDate(f)
    print "the date of event in tweet is ",date
    
    


