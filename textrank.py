# -*- coding: utf-8 -*-
from collections import OrderedDict
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.fr.stop_words import STOP_WORDS

#nlp = spacy.load('en_core_web_md')

nlp = spacy.load('fr_core_news_sm')

class TextRank4Keyword():
    """Extract keywords from text"""

    def __init__(self):
        self.d = 0.85  # damping coefficient, usually is .85
        self.min_diff = 1e-5  # convergence threshold
        self.steps = 10  # iteration steps
        self.node_weight = None  # save keywords and its weight

    def set_stopwords(self, stopwords):
        """Set stop words"""
        for word in STOP_WORDS.union(set(stopwords)):
            lexeme = nlp.vocab[word]
            lexeme.is_stop = True

    def sentence_segment(self, doc, candidate_pos, lower):
        """Store those words only in cadidate_pos"""
        sentences = []
        for sent in doc.sents:
            selected_words = []
            for token in sent:
                # Store words only with cadidate POS tag
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lower is True:
                        selected_words.append(token.text.lower())
                    else:
                        selected_words.append(token.text)
            sentences.append(selected_words)
        return sentences

    def get_vocab(self, sentences):
        """Get all tokens"""
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab

    def get_token_pairs(self, window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i + 1, i + window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs

    def symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())

    def get_matrix(self, vocab, token_pairs):
        """Get normalized matrix"""
        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1

        # Get Symmeric matrix
        g = self.symmetrize(g)

        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm != 0)  # this is ignore the 0 element in norm

        return g_norm

    def get_keywords(self, number=10):
        """Print top number keywords"""
        node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        for i, (key, value) in enumerate(node_weight.items()):
            print(key + ' - ' + str(value))
            if i > number:
                break

    def analyze(self, text,
                candidate_pos=['NOUN', 'PROPN'],
                window_size=4, lower=False, stopwords=list()):
        """Main function to analyze text"""

        # Set stop words
        self.set_stopwords(stopwords)

        # Pare text by spaCy
        doc = nlp(text)

        # Filter sentences
        sentences = self.sentence_segment(doc, candidate_pos, lower)  # list of list of words

        # Build vocabulary
        vocab = self.get_vocab(sentences)

        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)

        # Get normalized matrix
        g = self.get_matrix(vocab, token_pairs)

        # Initionlization for weight(pagerank value)
        pr = np.array([1] * len(vocab))

        # Iteration
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1 - self.d) + self.d * np.dot(g, pr)
            if abs(previous_pr - sum(pr)) < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]

        self.node_weight = node_weight

text = '''
<<Hhhhhhhh>>,- Les Restos du Cœur ont été fondés par Coluche en 1985. Depuis cette date, les gens les plus pauvres peuvent recevoir un repas gratuitement. L’association recueille des dons et des concerts sont même organisés chaque année pour couvrir les besoins. Chaque année le nombre de personnes qui demandent de l’aide aux Restos du Cœur augmente. L’année dernière, 87 millions de repas ont été servis à 700 000 personnes dans un des 1900 centres. Et depuis 1985, c’est un milliard de repas qui ont été servis. Pour les bénévoles des restos du cœur, même si le chômage baisse en France, le nombre de pauvres augmente toujours. Les Restos du cœur vont donc continuer à les aider à se sortir de la misère mais pas seulement en distribuant des repas.
Car l’association est en train d’évoluer, elle propose maintenant 175 chantiers et ateliers d’insertion pour aider les gens à retrouver un travail. Dans les maisons de Coluche, il y a des ateliers de menuiserie, de mécanique, la possibilité d’apprendre les métiers de la restauration ou les métiers des espaces verts. Ces chantiers d’insertion fonctionnent assez bien puisque 25% des gens qui en ont bénéficié ont retrouvé un travail.
Si vous allez en France pour étudier ou pour vous installer, vous verrez peut-être des bénévoles de l’association attendre devant un supermarché. Pour les aider, rien n’est plus simple, il vous suffit d’acheter un paquet de pâtes, une boîte de conserve ou du café en plus et le déposer dans leur caddie à la sortie.
'''
tr4w = TextRank4Keyword()
tr4w.analyze(text, candidate_pos=['NOUN', 'PROPN'], window_size=4, lower=False)
tr4w.get_keywords(10)