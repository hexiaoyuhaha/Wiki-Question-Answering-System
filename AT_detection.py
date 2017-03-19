import nltk
import re
import numpy as np
from scipy.sparse import hstack
from sklearn.svm import LinearSVC
from practnlptools.tools import Annotator
from sklearn.feature_extraction.text import CountVectorizer
from Helper import getPos, getNER

def read_file(filename):
    res = []
    with open(filename) as file:
        for line in file:
            res.append(line)
    return res

def global_setting():
    global folder 
    folder = 'data/'

def text_to_pos(source_file, tar_file):
    print '*****Text to PoS transformation begins*****'
    output = open(tar_file, 'w')
    with open(source_file) as file:
        k = 0
        for line in file:
            tokens = line.split()
            tags = getPos(tokens)
            tar = ''
            for i in tags:
                tar += i[1] + ' '
            k += 1
            if k % 500 == 0:
                print str(k) + ' samples extracted...'
            output.write(tar[:-1] + '\n')

def text_to_ner(source_file, tar_file):
    print '*****Text to NER transformation begins*****'
    output = open(tar_file, 'w')
    with open(source_file, 'r') as file:
        k = 0
        for line in file:
            tokens = line.split()
            ners = getNER(tokens)
            tar = ''
            for i in ners:
                tar += i[1] + ' '
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

def text_to_chunks(source_file, tar_file):
    print '*****Text to chunks transformation begins*****'
    output = open(tar_file, 'w')
    anno = Annotator()
    with open(source_file, 'r') as file:
        k = 0
        for line in file:
            ners = anno.getAnnotations(line[:-1])['chunk']
            tar = ''
            for i in ners:
                tar += i[1] + ' '
            k += 1
            if k % 500 == 0:
                print str(k) + ' samples extracted...'
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
    vector = CountVectorizer(ngram_range = (1, 1))
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

    label_set = set(Y_test)
    count_dict = {}
    hit_dict = {}
    count = 0
    for i in range(len(labels_test)):
        if Y_test[i] in count_dict:
            count_dict[Y_test[i]] += 1
        else:
            count_dict[Y_test[i]] = 1
        if labels_test[i] == Y_test[i]:
            if labels_test[i] in hit_dict:
                hit_dict[labels_test[i]] += 1
            else:
                hit_dict[labels_test[i]] = 1
            count += 1

    print "Total accuracy is ", (float)(count) / len(labels_test)
    for key, val in count_dict.iteritems():
        tmp = 0
        if key in hit_dict:
            tmp = float(hit_dict[key]) / val
        if tmp <= 0.5:
            print (key + ":%f") %tmp, val

def get_file_name(suffix):
    fn_list = ['words', 'PoS', 'NER', 'chunks']
    return [folder + i + suffix for i in fn_list]

def main():
    global_setting()
    train_fn_list = get_file_name('_train.txt')
    test_fn_list = get_file_name('_test.txt')
    train_source = folder + 'AT_train.txt'
    test_source = folder + 'AT_test.txt'

    # It takes a long time to run pos and ner extraction.
    # text_to_words(test_source, test_fn_list[0])
    # text_to_pos(test_fn_list[0], test_fn_list[1])
    # text_to_ner(test_fn_list[0], test_fn_list[2])
    # text_to_chunks(test_fn_list[0], test_fn_list[3])

    X_train, vectors = feature_construction(train_fn_list)
    Y_train = get_labels(train_source)

    X_test = feature_construction_test(test_fn_list, vectors)
    Y_test = get_labels(test_source)

    classify(X_train, Y_train, X_test, Y_test)



main()
