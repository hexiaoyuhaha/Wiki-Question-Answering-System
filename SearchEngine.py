import operator
from Article import Article
import Helper
import math
from textblob import TextBlob as tb

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
        self.query = query
        self.result = {}
        self.sortResult = []



    def rank(self):
        '''
        Main function of search engine.
        Compute the document score and store it in self.result and self.sortResult
        '''
        for index, sentence in enumerate(self.sentences):
            # self.result[index] = self.getDocScore(self.query, sentence)
            self.result[index] = self.getScoreIndri(self.query, sentence)
            #self.result[index] = self.getScoreTfidf(self.query, sentence)
        self.sortResult = sorted(self.result.items(), key=operator.itemgetter(1), reverse=True)



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


    def getScoreIndri(self, query, sentence):
        qargs = query.split()
        score = 1
        bloblist = [tb(doc.strip()) for doc in self.sentences]
        doc_len = sum(Helper.getLen(s) for s in self.sentences)
        for q in qargs:
            score *= self.getIndri(q, sentence, bloblist, doc_len)
        return math.pow(score, 1.0 / len(qargs))


    def getIndri(self, qarg, sentence, bloblist, doc_len):
        blob = tb(sentence.strip())
        tf = blob.words.count(qarg)
        ctf = sum(1 for blob in bloblist if qarg in blob.words)
        myLambda = 0.1
        myMu = 2500
        sentence_len = len(blob.words)
        # mle
        mle = ctf / float(doc_len)
        score = (1 - myLambda) * (tf + myMu * mle) / (sentence_len + myMu) + myLambda * mle
        return score


    def returnTopKResult(self, k):
        '''
        Return the top K ranking results
        '''
        topKSentences = [self.sentences[index] for index, score in self.sortResult[:k]]
        return topKSentences






article = Article('data/a1.htm')
query = 'New England Revolution selected eighth 2004'
se = SearchEngine(article, query)
se.rank()
print se.sortResult[:10]
for i in se.returnTopKResult(10):
    print i
