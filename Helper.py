from __future__ import division, unicode_literals
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob as tb
import math
from nltk.tag.stanford import StanfordPOSTagger
from nltk.tag import StanfordNERTagger
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
from nltk.stem.porter import PorterStemmer
import os


posTagger = StanfordPOSTagger('english-bidirectional-distsim.tagger')
nerTagger = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
parser = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
dep_parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
porter = PorterStemmer()

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

def getPos(words):
    return posTagger.tag(words)

def getNER(words):
    return nerTagger.tag(words)

def getParserTree(line):
    return list(parser.raw_parse(line))

def getDependencyTree(line):
    return [parse.tree() for parse in dep_parser.raw_parse(line)]

def getNouns(words):
    tags = getPos(words)
    res = []
    for (k,t) in tags:
        if str(t).startswith('NN'):
            res.append(str(k))
    return res


def getVerbs(words):
    tags = getPos(words)
    res = []
    for (k,t) in tags:
        if str(t).startswith('VB'):
            res.append(str(k))
    return res

def removeStopWords(words):
    return [word for word in words if word not in stopwords.words('english')]


def getStemWord(words):
    return [porter.stem(word) for word in words]

# for test purpose
'''
corpus = []
doc1 = "the quick brown fox jumps over the lazy dog"
doc2 = "What is the airspeed of an unladen swallow ?"
doc3 = "Rami Eid is studying at Stony Brook University in NY"
corpus.append(doc1)
corpus.append(doc2)


print 'tf', getTf('the',doc1)
print 'idf', getIdf('the', corpus)
print 'tfidf', getTfidf('the',doc1,corpus)
print 'pos', getPos(doc1.split())
print 'nouns', getNouns(doc1.split())
print 'verbs', getVerbs(doc1.split())
print 'ner', getNER(doc3.split())
print 'parse tree', getParserTree(doc1)
print 'dependency tree', getDependencyTree(doc1)
print 'remove stopwords', removeStopWords(doc2.split())
print 'stem word', getStemWord(doc3.split())
'''
