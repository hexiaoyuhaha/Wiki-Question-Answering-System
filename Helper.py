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


def getTf(word, blob):
    blob = tb(blob.strip())
    return blob.words.count(word)

def getLen(blob):
    blob = tb(blob.strip())
    return len(blob.words)

def getCtf(word, bloblist):
    bloblist = [tb(doc.strip('\n')) for doc in bloblist]
    return sum(1 for blob in bloblist if word in blob.words)


def getTfidf(word, blob, bloblist):
    blob = tb(blob.strip())
    bloblist = [tb(doc.strip()) for doc in bloblist]
    tf = blob.words.count(word) / len(blob.words)
    ctf = sum(1 for blob in bloblist if word in blob.words)
    idf = math.log(len(bloblist) / ctf) + 1
    return tf * idf


# for test purpose
'''
corpus = []
doc1 = "the quick brown fox jumps over the lazy dog"
doc2 = "What is the airspeed of an unladen swallow ?"
doc3 = "Rami Eid is studying at Stony Brook University in NY"
corpus.append(doc1)
corpus.append(doc2)
corpus.append(doc3)

print 'doc len', getLen(doc1)
print 'corpus len', sum(getLen(s) for s in corpus)
print 'tf', getTf('the',doc1)
print 'ctf', getCtf('the', corpus)
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
