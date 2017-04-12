import re
import sys
import json
import numpy as np
from scipy.sparse import hstack
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
import spacy

def global_setting():
    global folder 
    folder = 'data/'    

def text_to_pos(source_file, tar_file):
    print '*****Text to PoS transformation begins*****'
    output = open(tar_file, 'w')
    nlp = spacy.load('en')
    with open(source_file) as file:
        k = 0
        for line in file:
            line = unicode(line[:-1], "utf-8")
            tokens = nlp(line)
            tar = ''
            for tok in tokens:
                tar += tok.tag_ + ' '
            k += 1
            if k % 500 == 0:
                print str(k) + ' samples extracted...'
            output.write(tar[:-1] + '\n')

def text_to_ner(source_file, tar_file):
    print '*****Text to NER transformation begins*****'
    output = open(tar_file, 'w')
    nlp = spacy.load('en')
    with open(source_file, 'r') as file:
        k = 0
        for line in file:
            line = unicode(line[:-1], "utf-8")
            doc = nlp(line)
            tar = ''
            for ent in doc.ents:
                tar += ent.label_ + ' '
            k += 1
            if k % 500 == 0:
                print str(k) + ' samples extracted...'
            output.write(tar[:-1] + '\n')

def text_to_words(source_file, tar_file):
    print '*****Text to words transformation begins*****'
    output = open(tar_file, 'w')
    with open(source_file, 'r') as file:
        for line in file:
            tokens = re.sub(r"`",r"'",line).split()
            tar = ""
            for i in range(1, len(tokens) - 1):
                tar += tokens[i] + ' '
            output.write(tar[:-1] + '\n')

# Used to get labels of training set and test set
def get_labels(filename):
    labels = []
    with open(filename, 'r') as file:
        for line in file:
            labels.append(line.split()[0])
    return labels

# Used to get features of training set and test set
def vectorize(filename):
    docs = []
    with open(filename, 'r') as file:
        for line in file:
            docs.append(line)
    vector = CountVectorizer(ngram_range = (1, 2))
    return vector.fit_transform(docs), vector

def vectorize_test(filename, vector):
    docs = []
    with open(filename, 'r') as file:
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

    with open('data/AT_type_result.txt', 'w') as file:
        for label in labels_test:
            res = ''
            if label in mapping:
                res = mapping[label] + '\n'
            else:
                res = 'OTHER' + '\n'
            file.write(res)

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
    arg = sys.argv
    at_detect(arg[1])
