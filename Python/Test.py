from TF import *
from requeteMongo import *

docs = getTweetByTrend('#RainbowMW')
text = ''
for doc in docs:
    text += (doc['tweet_text'])

list = trigrams(text)
print(top(list,5))

list = bigrams(text)
print(top(list,5))

list = TF(text)
print(top(list,5))