import sys
from nltk.corpus import stopwords
from Article import *
from SearchEngine import *
from nltk import word_tokenize
import string
from AnswerExtraction import get_answer
from AT_detection import at_detect


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




verbose = True

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
    questions = readQuestions(questionFilePath)

    queries = [remove_stop_words(question) for question in questions]
    # queries = [question for question in questions]

    expected_types = at_detect(questionFilePath)
    print expected_types
    se = SearchEngine(article)
    for i, query in enumerate(queries):
        if verbose:
            print 'query:', query


        result = se.rankByIndri(query)
        topResults = se.returnTopKResult(result, 10)

        # Retrieve the top rankning answers
        for i in se.returnTopKResult(result, 10):
            if verbose:
                print i, se.sentences[i[0]]
            answer = answer(question)
            pred_answer = get_answer(question, expected_types[i], answer)


