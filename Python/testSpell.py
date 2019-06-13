from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize
from TF import *
import textdistance
"""
spell = SpellChecker(language = 'fr')
text = 'bonjour je suis venu manger'"""
text1 = 'bonsoir je suis parti manger'
"""print(textdistance.jaccard(text, text1))"""


from nltk.stem import WordNetLemmatizer
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer
#lemmatizer = FrenchLefffLemmatizer()
#print(lemmatizer.lemmatize('adadazdazdaefezfz ','all'))

print(stemText(text1))
