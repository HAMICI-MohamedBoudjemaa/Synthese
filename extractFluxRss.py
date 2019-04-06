import csv

import feedparser as fp
import json
import newspaper
from newspaper import Article
from time import mktime
from datetime import datetime


LIMIT = 10000000

data = {}
articles_array = []

# Charge le fichier Json contenant les liens
with open("./fichiers/linkRss.json") as data_file:
    linksNews = json.load(data_file)

count = 1

for linkNews, value in linksNews.items():

    # Si un lien RSS est fourni dans le fichier JSON, ce sera le premier choix.
    # La raison en est que les flux RSS donnent souvent des données plus cohérentes et correctes.
    # Si vous ne voulez pas extraire du flux RSS, laissez simplement le flux RSS vide dans le fichier JSON.
    if 'rss' in value:
        d = fp.parse(value['rss'])
        print("Telechargement articles pour ", linkNews)
        newsPaper = {
            "rss": value['rss'],
            "articles": []
        }

        for entry in d.entries:
            #print(entry.get("description"))
            # Vérifiez si la date de publication est fournie, sinon l’article est ignoré.
            # Ceci est fait pour maintenir la cohérence des données et pour empêcher le script de planter.
            if hasattr(entry, 'published'):
                if count > LIMIT:
                    break
                article = {}
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
                article['title'] = content.title
                #entry.get("description") : permet d'avoir que la description d'un article
                #article['text'] = entry.get("description")
                #content.text : permet d'avoir tout le texte de l'article
                article['text'] = content.text
                article['authors'] = content.authors
                article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
                article['link'] = entry.link

                newsPaper['articles'].append(article)
                articles_array.append(article)
                count = count + 1
    else:
        #si c'est lien simple, on utilise la bibliothèque de journaux Python pour extraire des articles
        paper = newspaper.build(value['link'], memoize_articles=False)
        newsPaper = {
            "link": value['link'],
            "articles": []
        }

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

            article = {}
            article['title'] = content.title
            # entry.get("description") : permet d'avoir que la description d'un article
            # article['text'] = entry.get("description")
            # content.text : permet d'avoir tout le texte de l'article
            article['text'] = content.text
            article['authors'] = content.authors
            article['link'] = entry.link
            article['published'] = content.publish_date
            newsPaper['articles'].append(article)
            count = count + 1

    count = 1
    data = newsPaper
    print(data)

    #enregistrer dans une les données extraites du flux rss dans un fichier CSV
    #!!!!!proposition : On pourra enregistrer dans une base de données et à chaque nouvelle extraction,
    # on efface l'ancienne données de la BD
    try:
        f = csv.writer(open('./fichiers/data_news_flux_rss_output.csv', 'w', encoding='utf-8'))
        f.writerow(['Title', 'Authors', 'Text', 'Link', 'Published_Date'])
        # print(article)
        for artist_name in articles_array:
            title = artist_name['title']
            authors = artist_name['authors']
            text = artist_name['text']
            link = artist_name['link']
            publish_date = artist_name['published']
            # Ajouter le nom de chaque artiste et le lien associé à une ligne
            f.writerow([title, authors, text, link, publish_date])
    except Exception as e:
        print(e)

