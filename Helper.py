from __future__ import division, unicode_literals
import nltk
from textblob import TextBlob as tb
import math
from nltk.tag.stanford import StanfordPOSTagger
from nltk.tag import StanfordNERTagger
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
import os


posTagger = StanfordPOSTagger('english-bidirectional-distsim.tagger')
nerTagger = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
parser = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
dep_parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

def getTf(word, blob):
    blob = tb(blob.strip())
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def getIdf(word, bloblist):
    bloblist = [tb(doc.strip('\n')) for doc in corpus]
    return math.log(len(bloblist) / n_containing(word, bloblist)) + 1

def getTfidf(word, blob, bloblist):
    return getTf(word, blob) * getIdf(word, bloblist)

def getPos(line):
    return posTagger.tag(line.split())

def getNER(line):
    return nerTagger.tag(line.split())

def getParserTree(line):
    return list(parser.raw_parse(line))

def getDependencyTree(line):
    return [parse.tree() for parse in dep_parser.raw_parse(line)]


# for test purpose
corpus = []
doc1 = "the quick brown fox jumps over the lazy dog"
doc2 = "What is the airspeed of an unladen swallow ?"
doc3 = "Rami Eid is studying at Stony Brook University in NY"
corpus.append(doc1)
corpus.append(doc2)
print 'tf',getTf('the',doc1)
print 'idf',getIdf('the', corpus)
print 'tfidf',getTfidf('the',doc1,corpus)
print getPos(doc2)
print getNER(doc3)
print getParserTree(doc1)
print getDependencyTree(doc1)
