import re
from urllib import parse as urlparse

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def clean_text(txt):
    #return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())
    txt = remove_emoji(txt)
    txt = re.sub(r"http[s]\S*", "",txt)
    txt = txt.replace('  ',' ')
    #txt = txt.replace('#','')
    return txt

"""def removeCaract(text):
    new_string = ''
    for i in text.split():
        s, n, p, pa, q, f = urlparse.urlparse(i)
        if s and n:
            pass
        elif i[:1] == '@':
            pass
        elif i[:1] == '#':
            new_string = new_string.strip() + ' ' + i[1:]
        elif i[:1] == 'htpps':            new_string = new_string.strip() + ' ' + i[1:]
        else:
            new_string = new_string.strip() + ' ' + i

    return new_string"""
    #return ' '.join(re.sub("([@#][A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

if __name__ == '__main__':
    print('---------------------------------------------')
    print(clean_text("Paris 13 c'est vrmt des chics types #Parcoursup #merci #vousmavezsauvé https://bit.ly//WjdiW# Côte d'Ivoire 🇨🇮❤  🤪🤩.️"))
    print('---------------------------------------------')
    #print(removeCaract("Paris 13 c'est vrmt des chics types #Parcoursup #merci #vousmavezsauvé https://bit.ly//WjdiW# Côte d'Ivoire 🇨🇮❤️"))
