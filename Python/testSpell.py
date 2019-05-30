from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize
from TF import *
import textdistance

spell = SpellChecker(language = 'fr')
text = 'bonjour je suis venu manger'
text1 = 'bonsoir je suis parti manger'
print(textdistance.jaccard(text, text1))
