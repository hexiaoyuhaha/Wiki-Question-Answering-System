import spacy
from settings import verbose

nlp = spacy.load('en')

is_types = ['is', 'was', 'are', 'were']
is_pos = ['is', 'was', 'are', 'were']
is_neg = ["isn't", "wasn't", "aren't", "weren't"]

do_types = ['did', 'do', 'does']
do_pos = ['did', 'do', 'does']
do_neg = ["didn't", "don't", "doesn't"]


def show_structure(doc):
    print doc
    for token in doc:
        print '%15s | %8d |% 10s | %15s' % (token.text, token.dep,
                                            token.dep_, token.head.text)
    print ''


def show(doc):
    print '-' * 10
    for word in doc:
        print word.text, word.lemma_, word.tag_, word.pos_, word.ent_type_


def show_noun_trunk(doc):
    print '-' * 10, 'show_noun_trunk'
    for word in doc.noun_chunks:
        print word.text


def show_noun(doc):
    print '-' * 10, 'show_noun'
    for word in doc:
        if word.pos_ in ['NOUN', 'PROPN']:
            print word.lemma_, word.tag_, word.pos_, word.ent_type_


def get_noun_lemma_no_person(doc):
    result = []
    for word in doc:
        if word.pos_ in ['NOUN', 'PROPN'] and word.ent_type_ != 'PERSON':
            result += [word.lemma_]
    return result


def get_noun_lemma(doc):
    result = []
    for word in doc:
        if word.pos_ in ['NOUN', 'PROPN']:
            result += [word.lemma_]
    return result


def get_yes_no_answer(text1, text2):
    doc1 = nlp(text1)
    doc2 = nlp(text2)

    # if verbose:
        # print 'show doc'
        # show(doc1)
        # show(doc2)

    doc1_nouns = get_noun_lemma_no_person(doc1)
    doc2_nouns = get_noun_lemma_no_person(doc2)
    doc1_names = find_person_name(doc1)

    if not doc1_nouns and not doc1_names:
        return 'EMPTY'

    if verbose:
        print '-' * 10
        print 'doc1_nouns', doc1_nouns
        print 'doc2_nouns', doc2_nouns

        print '-' * 10
        print 'doc1_names', doc1_names
        print '-' * 10

    for word in doc1_nouns:
        if word not in doc2_nouns:
            return 'No'

    for name in doc1_names:
        # if at least part of this name is contained in doc2
        # name = ['Alessandro', 'Volta']
        flag = False
        for token in name:
            if token in doc2.text:
                flag = True
                break
        if flag == False:
            return 'No'

    return 'Yes'


def find_person_name(doc):
    '''
    Return 2D array containing person name
    [['Xiaoyu', 'He'], ['Andrew', 'Ng']]
    '''
    names = []
    start = -1
    for i in range(len(doc)):
        if doc[i].ent_type_ == 'PERSON':
            if start == -1:
                start = i
        elif start != -1:
            name = [doc[k].text for k in range(start, i)]
            names.append(name)
            start = -1
    return names





# def main():
#     text1 = u'Was Alessandro Volta a professor of chemistry?'
#     text2 = u'In 1776-77 Volta studied the chemistry of gases, he discovered methane by collecting the gas from marshes.'
#     print noun_words_match(text1, text2)
#
#
# if __name__ == '__main__':
#     main()