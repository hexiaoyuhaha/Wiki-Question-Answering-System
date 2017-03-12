import operator

class SearchEngine:
    """
    SearchEngine class finds the best match sentences
    using given document and query

    Attributes:
        result: ranking result, dict {sentenceIdx: sentence score}
        sortResult: sorted ranking result, list of (index, score) tuple
        article: list of sentences
        query: list of query words
    """
    def __init__(self, article, query):
        '''
        Init the class with article and query
        :param article: input list of sentences
        :param query: list of query words, assuming no stop words in the query
        '''
        self.article = article
        self.query = query
        self.result = {}
        self.sortResult = []



    def rank(self):
        '''
        Main function of search engine.
        Compute the document score and store it in self.result and self.sortResult
        '''
        for index, sentence in enumerate(self.article):
            self.result[index] = self.getDocScore(self.query, sentence)

        self.sortResult = sorted(self.result.items(), key=operator.itemgetter(1), reverse=True)



    def getDocScore(self, query, sentence):
        '''
        compute the sentence score
        :param query: list of query words
        :param sentence: string
        :return: sentence score
        '''



    def returnTopKResult(self, k):
        '''
        Return the top K ranking results
        '''
        topKSentences = [self.article[index] for index, score in self.sortResult[:k]]
        return topKSentences

