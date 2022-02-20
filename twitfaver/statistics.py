import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk import bigrams, trigrams
import math


stopwords = ['for', 'is', 'of']
stopwords.extend(nltk.corpus.stopwords.words('indonesian'))
stopwords.extend(nltk.corpus.stopwords.words('english'))
tokenizer = RegexpTokenizer("[\w']+", flags=re.UNICODE)


def freq(word, doc):
    return doc.count(word)


def word_count(doc):
    return len(doc)


def tf(word, doc):
    return freq(word, doc) / float(word_count(doc))


def num_docs_containing(word, list_of_docs):
    count = 0
    for document in list_of_docs:
        if freq(word, document) > 0:
            count += 1
    return 1 + count


def idf(word, list_of_docs):
    return math.log(len(list_of_docs) / float(num_docs_containing(word, list_of_docs)))


def tf_idf(word, doc, list_of_docs):
    return tf(word, doc) * idf(word, list_of_docs)


def score_me(doc, min_score=None, bigram=True, trigram=True, count=10):
    tokens = tokenizer.tokenize(doc.lower())

    tokens = [token for token in tokens if len(token) > 2]
    tokens = [token for token in tokens if token not in stopwords]

    bi = tri = []

    if bigram:
        bi = bigrams(tokens)
        bi = [' '.join(token) for token in bi]
        bi = [token for token in bi if token not in stopwords]

    if trigram:
        tri = trigrams(tokens)
        tri = [' '.join(token) for token in tri]
        tri = [token for token in tri if token not in stopwords]

    clean = []
    clean.extend(tokens)

    if bigram:
        clean.extend(bi)

    if trigram:
        clean.extend(tri)

    score = {'freq': {}, 'tf': {}, 'idf': {}, 'tf-idf': {}, 'tokens': {}}

    for token in clean:
        score['freq'][token] = freq(token, clean)
        score['tf'][token] = tf(token, clean)
        score['tokens'] = clean
        score['idf'][token] = idf(token, clean)

        val = tf_idf(token, clean, clean)
        if val >= min_score:
            score['tf-idf'][token] = val

    final = {}
    for token in score['tf-idf']:
        if token not in final:
            final[token] = score['tf-idf'][token]
        else:
            if score['tf-idf'][token] > final[token]:
                final[token] = score['tf-idf'][token]

    return [item for item in sorted(final.items(), key=lambda x: x[1], reverse=True)[:count]]
