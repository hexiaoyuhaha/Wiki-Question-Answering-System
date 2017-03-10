from __future__ import division, unicode_literals
import nltk
from textblob import TextBlob as tb
import math
from nltk.tag.stanford import StanfordPOSTagger
from nltk.tag import StanfordNERTagger
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser

corpus = []
doc1 = "I love Chinese food"
doc2 = "I love American spirits"
corpus.append(doc1)
corpus.append(doc2)


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
    st = StanfordPOSTagger('english-bidirectional-distsim.tagger')
    print st.tag('What is the airspeed of an unladen swallow ?'.split())

def getNER(line):
    st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
    print st.tag('Rami Eid is studying at Stony Brook University in NY'.split())


def getParserTree(line):
    parser=StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    print list(parser.raw_parse("the quick brown fox jumps over the lazy dog"))

def getDependencyTree(line):
    dep_parser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    print [parse.tree() for parse in dep_parser.raw_parse("The quick brown fox jumps over the lazy dog.")]

print 'tf',getTf('love',doc1)
print 'idf',getIdf('love', corpus)
print 'tfidf',getTfidf('love',doc1,corpus)

#getPos(doc1)
#getNER(doc1)
getParserTree(doc1)
#getDependencyTree(doc1)
