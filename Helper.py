from __future__ import division, unicode_literals
import nltk
from textblob import TextBlob as tb
import math

corpus = []
doc1 = "I love Chinese food"
doc2 = "I love American spirits"
corpus.append(doc1)
corpus.append(doc2)
print 'tf',tf('love',doc1)
print 'idf',idf('love', corpus)
print 'tfidf',tfidf('love',doc1,corpus)

def getTf(word, blob):
    blob = tb(blob.strip())
    return blob.words.count(word) / len(blob.words)



def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def getIdf(word, bloblist):
    bloblist = [tb(doc.strip('\n')) for doc in corpus]
    return math.log(len(bloblist) / n_containing(word, bloblist)) + 1

def getTfIdf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)
