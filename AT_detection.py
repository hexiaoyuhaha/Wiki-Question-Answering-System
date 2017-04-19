import codecs
import re
import sys
import json
import numpy as np
from scipy.sparse import hstack
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
import spacy

verbose = False

def global_setting():
    global folder 
    folder = 'data/'
    global mod
    mod = {}   

def text_to_pos(source_file, tar_file):
    if verbose:
        print '*****Text to PoS transformation begins*****'
    output = open(tar_file, 'w')
    nlp = spacy.load('en')
    with open(source_file) as file:
        for line in file:
            line = unicode(line[:-1], encoding='utf-8', errors='ignore')
            tokens = nlp(line)
            tar = ''
            for tok in tokens:
                tar += tok.tag_ + ' '
            output.write(tar[:-1] + '\n')

def text_to_ner(source_file, tar_file):
    if verbose:
        print '*****Text to NER transformation begins*****'
    output = open(tar_file, 'w')
    nlp = spacy.load('en')
    with open(source_file, 'r') as file:
        for line in file:
            line = unicode(line[:-1],encoding='utf-8', errors='ignore')
            doc = nlp(line)
            tar = ''
            for ent in doc.ents:
                tar += ent.label_ + ' '
            output.write(tar[:-1] + '\n')

def text_to_words(source_file, tar_file):
    if verbose:
        print '*****Text to words transformation begins*****'
    output = open(tar_file, 'w')
    with open(source_file, 'r') as file:
        k = 0
        for line in file:
            line = line.strip()
            if line:
                tokens = re.sub(r"`",r"'",line).split()
                tar = ""
                for i in range(len(tokens) - 1):
                    tar += tokens[i] + ' '
                if len(tokens) < 1:
                    print 'haha'
                modify(tokens[0], k)
                k += 1
                output.write(tar[:-1] + '\n')

def modify(token, k):
    token = token.lower()
    if token == 'when':
        mod[k] = 'DATE'
    elif token == 'where':
        mod[k] = 'GPE'
    elif token == 'who':
        mod[k] = 'PERSON'


# Used to get labels of training set and test set
def get_labels(filename):
    labels = []
    with codecs.open(filename, "r",encoding='utf-8', errors='ignore') as file:
        for line in file:
            labels.append(line.split()[0])
    return labels

# Used to get features of training set and test set
def vectorize(filename):
    docs = []
    with codecs.open(filename, "r",encoding='utf-8', errors='ignore') as file:
        for line in file:
            docs.append(line)
    vector = CountVectorizer(ngram_range = (1, 2))
    return vector.fit_transform(docs), vector

def vectorize_test(filename, vector):
    docs = []
    with codecs.open(filename, "r",encoding='utf-8', errors='ignore') as file:
        for line in file:
            docs.append(line)
    return vector.transform(docs)

def feature_construction(fn_list):
    vectors = []
    features, word_vector = vectorize(fn_list[0])
    vectors.append(word_vector)
    for i in range(1, len(fn_list)):
        tmp, vect = vectorize(fn_list[i])
        features = hstack((features, tmp))
        vectors.append(vect)
    return features, vectors

def feature_construction_test(fn_list, vectors):
    features = vectorize_test(fn_list[0], vectors[0])
    for i in range(1, len(fn_list)):
        features = hstack((features, vectorize_test(fn_list[i], vectors[i])))
    return features

def classify(X_train, Y_train, X_test, Y_test):
    classifier = LinearSVC()
    classifier = LinearSVC.fit(classifier, X_train, Y_train)
    labels_test = LinearSVC.predict(classifier, X_test)

    mapping = {}
    with open('data/mapping.json', 'r') as file:
        mapping = json.loads(file.read())

    result = []
    with open('data/AT_type_result.txt', 'w') as file:
        for label in labels_test:
            res = ''
            if label in mapping:
                res = mapping[label] + '\n'
            else:
                res = 'OTHER' + '\n'
            file.write(res)
            result.append(res[:-1])
    # for key, val in mod.iteritems():
    #     result[i] = val
    return result
    count = 0
    for i in range(len(labels_test)):
        if labels_test[i] == Y_test[i]:
            count += 1
    print "accuracy is ", (float)(count) / len(labels_test)


def get_file_name(suffix):
    fn_list = ['words', 'PoS', 'NER']
    return [folder + i + suffix for i in fn_list]

def at_detect(filename):
    global_setting()
    train_fn_list = get_file_name('_train.txt')
    predict_fn_list = get_file_name('_predict.txt')
    train_source = folder + 'AT_train.txt'
    predict_source = filename

    # It takes a long time to run pos and ner extraction.
    # text_to_words(train_source, train_fn_list[0])
    # text_to_pos(train_fn_list[0], train_fn_list[1])
    # text_to_ner(train_fn_list[0], train_fn_list[2])

    text_to_words(predict_source, predict_fn_list[0])
    text_to_pos(predict_fn_list[0], predict_fn_list[1])
    text_to_ner(predict_fn_list[0], predict_fn_list[2])

    X_train, vectors = feature_construction(train_fn_list)
    Y_train = get_labels(train_source)

    X_test = feature_construction_test(predict_fn_list, vectors)
    Y_test = get_labels(predict_source)

    return classify(X_train, Y_train, X_test, Y_test)

def difficulty_detect():
    global_setting()
    train_fn_list = get_file_name('_diff_train.txt')
    predict_fn_list = get_file_name('_diff_predict.txt')
    train_source = folder + 'difficulty_train.txt'
    predict_source = folder + 'difficulty_test.txt'

    text_to_words(train_source, train_fn_list[0])
    text_to_pos(train_fn_list[0], train_fn_list[1])
    text_to_ner(train_fn_list[0], train_fn_list[2])
    text_to_words(predict_source, predict_fn_list[0])
    text_to_pos(predict_fn_list[0], predict_fn_list[1])
    text_to_ner(predict_fn_list[0], predict_fn_list[2])

    X_train, vectors = feature_construction(train_fn_list)
    Y_train = get_labels(train_source)

    X_test = feature_construction_test(predict_fn_list, vectors)
    Y_test = get_labels(predict_source)
    classify(X_train, Y_train, X_test, Y_test)


if __name__ == '__main__':
    # difficulty_detect()
    # arg = sys.argv
    arg = ['', 'data/AT_test.txt']
    at_detect(arg[1])
