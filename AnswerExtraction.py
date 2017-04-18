import spacy

class AnswerExtraction:
    verbose = False

    def __init__(self):
        self.nlp = spacy.load('en')


    def get_ner_token_pair(self, text):
        '''Careful! NER tag is case sensitive'''
        doc = self.nlp(text)
        result = []
        for ent in doc.ents:
            result += [(ent.label_, ent.text)]
        return result


    def get_answer(self, question, expected_type, retrieved_passage):
        '''
        where, who, when
        :param question:
        :param expected_type:
        :param retrieved_passage:
        :return:
        '''
'''
    if token == 'when':
        mod[k] = 'DATE'
    elif token == 'where':
        mod[k] = 'GPE'
    elif token == 'who':
        mod[k] = 'PERSON'
'''
        if expected_type in ['GPE', 'LOC'] or question.lower().strip().startswith("where"):
            potent_types = ['GPE', 'LOC']
        elif expected_type in ['GPE', 'LOC'] or question.lower().strip().startswith("where"):
            potent_types = ['GPE', 'LOC']
        elif expected_type in ['GPE', 'LOC'] or question.lower().strip().startswith("where"):
                    potent_types = ['GPE', 'LOC']
        elif expected_type == 'OTHER':
            return '/'
        else:
            potent_types = [expected_type]

        ner_token_pair = self.get_ner_token_pair(unicode(retrieved_passage))
        if self.verbose:
            print 'NER token:',ner_token_pair
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


    # for each record, find it's answer
    count_right = 0
    count_empty = 0
    for question, answer in train_data:
        print '=='
        ansextr = AnswerExtraction()
        pred_answer = ansextr.get_answer(question, 'LOC', answer)
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
