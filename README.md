<b>Synthese</b>

EXTRACTION DES ARTICLES VIA FLUX RSS OU LES LIENS SANS FLUX RSS :

Dans le fichiers se trouve un fichier Json contenant la liste des liens pour l'extraction des articles
Vous pouvez ajoutez des liens flux rss ou des liens simple :

Exemple :

Pour le flux rss : "rss"

 "rss":"http://www.lefigaro.fr/rss/figaro_politique.xml"
 
Pour des liens sans flux rss : "link"

"link": "http://www.bbc.com/"


<b>Les liens pour installer les packages :</b>

<color="blue">pip3 install spacy</color>

sudo apt-get install python3-setuptools

python3 -m spacy download en_core_web_sm

python3 -m spacy download en_core_web_md

python3 -m spacy download fr_core_news_sm

