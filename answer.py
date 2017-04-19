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



def main(argv):
    try:
        inputFilePath = argv[1]
        questionFilePath = argv[2]
    except:
        print "ERROR: Unable to read input argument!!"
        inputFilePath = 'data/a1.txt'
        questionFilePath = 'ques1.txt'
        # exit(1)


    article = Article(inputFilePath)

    # Get questions, queries, expected_types
    questions = readQuestions(questionFilePath)
    expected_types = at_detect(questionFilePath)
    queries = [remove_stop_words(question) for question in questions]

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

            answer = ansextr.get_answer(questions[i], expected_types[i], sentence)
            if answer != '/':
                finalAnswer = answer
                break
        if verbose:
            print '==finalAnswer==:', finalAnswer
        else:
            print finalAnswer


if __name__ == '__main__':
    main(sys.argv)



