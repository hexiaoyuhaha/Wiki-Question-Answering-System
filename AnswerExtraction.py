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

    '''
        if token == 'when':
            mod[k] = 'DATE'
        elif token == 'where':
            mod[k] = 'GPE'
        elif token == 'who':
            mod[k] = 'PERSON'
    '''
    def get_answer(self, question, expected_type, retrieved_passage):
        '''
        where, who, when
        :param question:
        :param expected_type:
        :param retrieved_passage:
        :return:
        '''
        location_types = ['GPE', 'LOC']
        date_types = ['DATE', 'TIME']
        person_types = ['PERSON', 'NORP']
        if expected_type in location_types or question.lower().strip().startswith("where"):
            potent_types = location_types
        elif expected_type in date_types or question.lower().strip().startswith("when"):
            potent_types = date_types
        elif expected_type in person_types or question.lower().strip().startswith("who"):
            potent_types = person_types
        elif expected_type == 'OTHER':
            return get_anwer_other(question, retrieved_passage)
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


    def get_anwer_other(self, question, retrieved_passage):
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
        if headword in ['is', 'was']:
            return 'yes'
        elif headword in ['did', 'do', 'does']:
            return 'yse'
        elif headword == 'what':
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
