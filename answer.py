import sys
from nltk.corpus import stopwords
from Article import Article
from SearchEngine import SearchEngine
from nltk import word_tokenize
import string
from AnswerExtraction import AnswerExtraction
from AT_detection import at_detect


verbose = True
RETRIEVAL_LIMIT = 5


def readQuestions(questionFilePath):
    """Read questions from file."""
    with open(questionFilePath) as infile:
        lines = infile.readlines()
        output = [line.strip() for line in lines]
        return output


def remove_stop_words(sentence):
    """Remove stop words"""
    #get words
    example_words = word_tokenize(sentence)
    #remove punctuation
    example_words = filter(lambda x: x not in string.punctuation, example_words)
    #remove stopwords
    example_words = [word for word in example_words if word not in stopwords.words('english')]
    return ' '.join(example_words)





if __name__ == '__main__':
    try:
        inputFilePath = sys.argv[1]
        questionFilePath = sys.argv[2]
    except:
        print "ERROR: Unable to read input argument!!"
        # exit(1)

    inputFilePath = 'data/a1.txt'
    questionFilePath = 'data/a1-question.txt'
    article = Article(inputFilePath)

    # Get questions, queries, expected_types
    questions = readQuestions(questionFilePath)
    queries = [remove_stop_words(question) for question in questions]
    expected_types = at_detect(questionFilePath)
    # expected_types = ['PERSON']
    assert len(expected_types) == len(questions)
    assert len(expected_types) == len(queries)


    # Init classes
    se = SearchEngine(article)
    ansextr = AnswerExtraction()
    ansextr.verbose = verbose

    for i in range(len(queries)):
        if verbose:
            print 'query:', queries[i]

        result = se.rankByIndri(queries[i])
        topSentence = se.returnTopKResult(result, RETRIEVAL_LIMIT)

        finalAnswer = ''
        # Retrieve the top rankning answers
        for sentence in topSentence:
            if verbose:
                print 'questions[i]: %s\nqueries[i]: %s\n expected_types: %s\n sentence:%s' \
                      % (questions[i], queries[i], expected_types[i], sentence)

            answer = ansextr.get_answer(question[i], expected_types[i], sentence)
            if answer != '/':
                finalAnswer = answer
                break
        print finalAnswer



