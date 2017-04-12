import operator
from Article import Article
import Helper
import math
from textblob import TextBlob as tb
from collections import defaultdict
from nltk.tokenize import wordpunct_tokenize
#from nltk.tokenize import

class SearchEngine:
    """
    SearchEngine class finds the best match sentences
    using given document and query

    Attributes:
        result: ranking result, dict {sentenceIdx: sentence score}
        sortResult: sorted ranking result, list of (index, score) tuple
        article: Article
        query: list of query words
    """
    def __init__(self, article, query):
        '''
        Init the class with article and query
        :param article: input list of sentences
        :param query: list of query words, assuming no stop words in the query
        '''
        self.article = article
        self.sentences = article.getRawLines()
        self.qargs = wordpunct_tokenize(query)
        self.result = defaultdict(float)
        self.doc_len = 0
        self.myLambda = 0.1
        self.myMu = 2500
        # {word: {docid: [doclen, tf],...}
        self.invertedList = defaultdict(dict)
        self.initiateInvertedList()


    def initiateInvertedList(self):
        bloblist = [tb(sent.strip()) for sent in self.sentences]
        for sentid, blob in enumerate(bloblist):
            sent_len = len(blob.words)
            self.doc_len += sent_len
            for word in blob.words:
                tf = blob.words.count(word)
                self.invertedList[word][sentid] = (sent_len, tf)



    """
    def rank(self):

        #Main function of search engine.
        #Compute the document score and store it in self.result and self.sortResult

        for index, sentence in enumerate(self.sentences):
            # self.result[index] = self.getDocScore(self.query, sentence)
            self.result[index] = self.getScoreIndri(self.query, sentence)
            #self.result[index] = self.getScoreTfidf(self.query, sentence)
        self.sortResult = sorted(self.result.items(), key=operator.itemgetter(1), reverse=True)
        '''

    def getDocScore(self, query, sentence):
        '''
        compute the sentence score
        :param query: list of query words
        :param sentence: string
        :return: sentence score
        '''
        return



    def getScoreTfidf(self, query, sentence):
        '''
        compute the sentence score
        :param query: list of query words
        :param sentence: string
        :return: sentence score
        '''
        qargs = query.split()
        score = 0
        bloblist = [tb(doc.strip()) for doc in self.sentences]
        for q in qargs:
            score += self.getTfidf(q, sentence, bloblist)
        return score


    def getTfidf(self, word, blob, bloblist):
        blob = tb(blob.strip())
        tf = blob.words.count(word) / float(len(blob.words))
        ctf = sum(1 for blob in bloblist if word in blob.words)
        idf = math.log(len(bloblist) / float(ctf)) + 1
        return tf * idf
        """


    def rankByIndri(self):
        #print self.invertedList
        for q in self.qargs:
            sents = self.invertedList[q]
            ctf = len(sents)
            mle = ctf / float(self.doc_len)
            for sentid, s in enumerate(self.sentences):
                # initiate score
                if sentid not in self.result:
                    self.result[sentid] = 1.0
                if sentid in sents:
                    sent_len = sents[sentid][0]
                    tf = sents[sentid][1]
                    self.result[sentid] *= (1 - self.myLambda) * (tf + self.myMu * mle) / (sent_len + self.myMu) + self.myLambda * mle
                else:
                    sent_len = len(tb(s.strip()).words)
                    self.result[sentid] *= (1-self.myLambda) * (self.myMu * mle) / (sent_len + self.myMu) + self.myLambda * mle
        for sentid, score in self.result.iteritems():
            self.result[sentid] = math.pow(score, 1.0 / len(self.qargs))



    def returnTopKResult(self, k):
        '''
        Return the top K ranking results
        '''
        topKSentences = sorted(self.result.items(), key=lambda d: -d[1])[:k]
        return topKSentences



if __name__ == '__main__':
    article = Article('data/a1.htm')
    query = 'New England Revolution selected eighth 2004'
    se = SearchEngine(article, query)
    se.rankByIndri()
    for i in se.returnTopKResult(10):
        print i,se.sentences[i[0]]
