import spacy

nlp = spacy.load('en')

'''
Careful! NER tag is case sensitive
'''
def get_ner_token_pair(text):
    doc = nlp(text)
    result = []
    for ent in doc.ents:
        result += [(ent.label_, ent.text)]
    return result


def get_answer(question, potent_types, retrieved_passage):
    ner_token_pair = get_ner_token_pair(unicode(retrieved_passage))
    print retrieved_passage
    print ner_token_pair
    if ner_token_pair:
        for ner, token in ner_token_pair:
            if ner in potent_types:
                return token
    return '/'


def read_data(filepath):
    '''
    Input data format:
    Alessandro_Volta	Where was Volta born?	Como	medium	medium	data/set4/a10

    Output dataformat:
    List of tuples like this: (Where was Volta born?	Como)
    '''
    with open(filepath) as infile:
        lines = infile.readlines()
        data = [(line.split('\t')[1].strip(), line.split('\t')[2].strip())
                for line in lines if 'NULL' not in line]
    return data


if __name__ == '__main__':
    # Where question
    # training data, list of tuple(queston, answer)
    train_data = read_data("data/AnsEx_train_where.txt")
    # train_data = [('','Bullet ants are located in Central and South America.')]
    m = len(train_data)
    potential_tag = ['GPE', 'LOC']

    # for each record, find it's answer
    count_right = 0
    count_empty = 0
    for question, answer in train_data:
        print '=='
        pred_answer = get_answer(question, potential_tag, answer)
        if pred_answer in answer:
            print '+', pred_answer
            count_right += 1
        else:
            if (pred_answer == '/'):
                count_empty += 1
            print '-', pred_answer
    print '***************'
    print 'correct rate:', 1. * count_right / m
    print 'false rate:', 1. * (m - count_right - count_empty) / m
    print 'empty rate:', 1. * count_empty / m
