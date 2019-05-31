import feedparser as fp
import json
import newspaper
from newspaper import Article
from time import mktime
from datetime import datetime
from Python.connexionLocal import *
from Python.gestion_logging import log_message

LIMIT = 10000000

# Charge le fichier Json contenant les liens
def loadJsonLink():
    with open("/home/ucp/PycharmProjects/Synthese/fichiers/linkRss.json") as data_file:
        linksNews = json.load(data_file)
    return linksNews



def extractDataFlux():
    articles_array = []
    count = 1
    for linkNews, value in loadJsonLink().items():
        # Si un lien RSS est fourni dans le fichier JSON, ce sera le premier choix.
        # La raison en est que les flux RSS donnent souvent des données plus cohérentes et correctes.
        # Si vous ne voulez pas extraire du flux RSS, laissez simplement le flux RSS vide dans le fichier JSON.
        if 'rss' in value:
            d = fp.parse(value['rss'])
            print("Telechargement articles pour ", linkNews)
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
                        # le prochain article.
                        print(e)
                        print("continu...")
                        continue
                    title = content.title
                    description = entry.get("description")
                    published = datetime.fromtimestamp(mktime(date)).isoformat()
                    #contenu = content.text

                    data = {'id_link': rss,'titre':title, 'description':description, 'date_publication':published }
                    fluxRSS.save(data)
                    log_message(data,'info')
                    count = count + 1
        else:
            #si c'est lien simple, on utilise la bibliothèque de journaux Python pour extraire des articles
            paper = newspaper.build(value['link'], memoize_articles=False)
            link = value['link']
            for content in paper.articles:
                if count > LIMIT:
                    break
                try:
                    content.download()
                    content.parse()
                except Exception as e:
                    print(e)
                    print("continue...")
                    continue

                # Encore une fois, par souci de cohérence, s'il n'y a pas de date de publication trouvée, l'article sera ignoré.
                # Après 10 articles téléchargés du même journal sans date de publication, la société sera ignorée.
                if content.publish_date is None:
                    print(count, " L'article a une date de type Aucun ")
                    noneTypeCount = noneTypeCount + 1
                    if noneTypeCount > 10:
                        print("Trop de dates noneType...")
                        noneTypeCount = 0
                        break
                    count = count + 1
                    continue

                title = content.title
                description = entry.get("description")
                #contenu = content.text
                published = content.publish_date
                data = {'link': link, 'titre': title, 'description': description, 'date_publication': published, 'type':''}
                fluxRSS.save(data)
                log_message(data, 'info')
                count = count + 1

        count = 1

if __name__ == '__main__':
    extractDataFlux()