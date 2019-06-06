import json
from datetime import datetime
from time import mktime

import feedparser as fp
from connnexionMongo import *
from gestion_logging import log_message
from newspaper import Article
from requeteMongo import *

LIMIT = 10000000

# Charge le fichier Json contenant les liens
def loadJsonLink():
    with open("/home/ucp/PycharmProjects/Synthese/fichiers/linkRss.json") as data_file:
        linksNews = json.load(data_file)
    return linksNews

def extractDataFlux():
    articles_array = []
    count = 1
    for linkNews, values in loadJsonLink().items():
        print("Telechargement articles type ", linkNews)
        for value in values:
            # Si un lien RSS est fourni dans le fichier JSON, ce sera le premier choix.
            # La raison en est que les flux RSS donnent souvent des données plus cohérentes et correctes.
            # Si vous ne voulez pas extraire du flux RSS, laissez simplement le flux RSS vide dans le fichier JSON.
            if 'rss' in value:
                d = fp.parse(value['rss'])
                log_message(value['rss'], 'warn')
                rss = value['rss']
                for entry in d.entries:
                    #print(entry.get("description"))
                    # Vérifiez si la date de publication est fournie, sinon l’article est ignoré.
                    # Ceci est fait pour maintenir la cohérence des données et pour empêcher le script de planter.
                    if hasattr(entry, 'published'):
                        if count > LIMIT:
                            break
                        date = entry.published_parsed
                        try:
                            content = Article(entry.link)
                            content.download()
                            content.parse()
                        except Exception as e:
                            # Si le téléchargement échoue pour une raison quelconque (ex. 404), le script continue le téléchargement.
                            # le proc   hain article.
                            print(e)
                            print("continu...")
                            continue
                        title = content.title
                        description = entry.get("description")
                        published = datetime.fromtimestamp(mktime(date)).isoformat()
                        #contenu = content.text
                        data = {'rss_link': rss, 'titre': title, 'description': description,
                                'date_publication': published, 'type': linkNews}
                        if findIfFluxRSSExist(rss,title,description,published, linkNews ) > 0:
                            log_message("Données déjà en base de donnée " + str(data), "error")
                        else:
                            log_message(data, 'info')
                            fluxRSS.save(data)

                        count = count + 1

if __name__ == '__main__':
    #print(loadJsonLink())
    #print(json.dumps(loadJsonLink(), indent=4))
    extractDataFlux()
