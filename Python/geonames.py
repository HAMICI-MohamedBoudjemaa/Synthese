import requests
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def isPlace(str):
    url = 'http://api.geonames.org/search'
    username = 'hongphuc95'
    maxRows = '5'
    q = str
    #fuzzy = '0.8'  # Precision
    type = 'json'
    lang = 'en'  # Anglais par defaut

    response = requests.get(
        url,
        params=
        {
            'username': username,
            'maxRows': maxRows,
            'type': type,
            'q': q,
        }
    )

    data = response.json()
    #if response.status_code == 200:
    #    #TODO
    #elif response.status_code == 404:
    #    print('404 Pas Trouve.')
    #else:
    #    print('Oopsie doopsie')
    #
    if data is not None:
        if not data['geonames']:
            return 'Nope'
        else :
            if len(str.split()) == 1:
                nameLookupDict = {};
                for dataGeo in data['geonames']:
                    nameLookup = dataGeo['name']
                    fuziness = fuzz.ratio(str, nameLookup)
                    nameLookupDict[nameLookup] = fuziness
                    for name in nameLookupDict:
                        if nameLookupDict[name] > 80:
                            return 'Passed'
                            break
                        return 'Considered'
            elif len(str.split()) == 2:
                for dataGeo in data['geonames']:
                    nameLookup = dataGeo['name']
                    fuziness = fuzz.ratio(str, nameLookup)
                    if fuziness > 80:
                        return 'Passed'
                    else:
                        return 'Nope'
    else:
        return None


if __name__ == '__main__':
    text = "WASHINGTON — At a meeting of President Trump’s top national security aides last Thursday, Acting Defense Secretary Patrick Shanahan presented an updated military plan that envisions sending as many as 120,000 troops to the Middle East should Iran attack American forces or accelerate work on nuclear weapons, administration officials said.[To follow new military deployments to the Middle East, sign up for the weekly At War newsletter.] The revisions were ordered by hard-liners led by John R. Bolton, Mr. Trump’s national security adviser. They do not call for a land invasion of Iran, which would require vastly more troops, officials said. The development reflects the influence of Mr. Bolton, one of the administration’s most virulent Iran hawks, whose push for confrontation with Tehran was ignored more than a decade ago by President George W. Bush. It is highly uncertain whether Mr. Trump, who has sought to disentangle the United States from Afghanistan and Syria, ultimately would send so many American forces back to the Middle East."
    #text = '14 mai 1610. Le Mans du roi Henri IV est bloqué rue de la Ferronnerie, à Paris, par une charrette de foin. Ravaillac en profite pour monter sur une des roues et poignarde le roi !Ravaillac sera torturé, écartelé, brûlé, et ses cendres jetées au vent.'
    textArray = re.split(' |\. |, ', text)
    lastWord = None
    for word in textArray:
        if re.search('^#.*', word):
            word = word.replace('#', '')
            #if word.istitle() or word.isupper() :
        if isPlace(word) == 'Passed':
            print("{} is a place".format(word))
            lastWord = None
        else:
            if lastWord is not None:
                newStr = lastWord + " " + word
                if isPlace(newStr) == 'Passed':
                    print("{} is a place".format(newStr))
                    lastWord = None
                else:
                    if isPlace(word) == 'Considered':
                        lastWord = word
            else:
                if isPlace(word) == 'Considered':
                    lastWord = word








