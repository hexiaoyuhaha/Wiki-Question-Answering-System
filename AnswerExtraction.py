import spacy
from AnswerExtractionYesNo import get_yes_no_answer

location_types = ['GPE', 'LOC']
date_types = ['DATE', 'TIME']
person_types = ['PERSON', 'NORP']

is_types = ['is', 'was', 'are', 'were']
is_pos = ['is', 'was', 'are', 'were']
is_neg = ["isn't", "wasn't", "aren't", "weren't"]

do_types = ['did', 'do', 'does']
do_pos = ['did', 'do', 'does']
do_neg = ["didn't", "don't", "doesn't"]

nlp = spacy.load('en')
verbose = True


def get_ner_token_pair(text):
    '''Careful! NER tag is case sensitive'''
    doc = nlp(text)
    result = []
    for ent in doc.ents:
        result += [(ent.label_, ent.text)]
    return result


def get_NER_answer(potent_types, retrieved_passage):
    ner_token_pair = get_ner_token_pair(unicode(retrieved_passage))
    if verbose:
        print 'NER token:',ner_token_pair
    if ner_token_pair:
        for ner, token in ner_token_pair:
            if ner in potent_types:
                return token
    return '/'


def get_answer(question, expected_type, retrieved_passage):
    '''
    where, who, when
    :param question:
    :param expected_type:
    :param retrieved_passage:
    :return:
    '''
    headword = question.split(" ")[0].lower()
    if headword in is_types or headword in do_types:
        result = get_yes_no_answer(question, retrieved_passage)
        if result == 'EMPTY':
            return retrieved_passage
        else:
            return result  # Yes, No
    elif expected_type in ['OTHER', 'CARDINAL']:
        return get_anwer_other(question, retrieved_passage)
    elif expected_type in location_types or question.lower().strip().startswith("where"):
        potent_types = location_types
        get_NER_answer(potent_types, retrieved_passage)
    elif expected_type in date_types or question.lower().strip().startswith("when"):
        potent_types = date_types
        get_NER_answer(potent_types, retrieved_passage)
    elif expected_type in person_types or question.lower().strip().startswith("who"):
        potent_types = person_types
        return retrieved_passage
    else:
        return retrieved_passage




def get_anwer_other(question, retrieved_passage):
    '''
    Is Avogadro's number used to compute the results of chemical reactions?
    Was Alessandro Volta a professor of chemistry?

    Did Alessandro Volta invent the remotely operated pistol?
    Do male ants take flight before females?

    What did Alessandro Volta invent in 1800?

    :param question:
    :param retrieved_passage:
    :return:
    '''
    headword = question.split(" ")[0].lower()
    return retrieved_passage



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


    # for each record, find it's answer
    count_right = 0
    count_empty = 0
    for question, answer in train_data:
        print '=='
        pred_answer = get_answer(question, 'LOC', answer)
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
