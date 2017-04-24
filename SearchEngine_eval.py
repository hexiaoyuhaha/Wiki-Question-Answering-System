from collections import defaultdict
from Article import Article
from SearchEngine import SearchEngine
import codecs

# Select only the selected 50 sentences
# compute the acurracy
# 2017-04-24 09:34:02,380 INFO ORIGINAL Berlin is the capital city and one of 16 states of Germany 
# 2017-04-24 09:34:02,509 INFO NP VP(subject) What is the capital city and one of 16 states of Germany ?


def show(sent_ques):
    for k, v in sent_ques.items():
        print k
        for s in v:
            print '\t%s' % s


def go(quesfile, logFile, inputFilePath):
    top_50_ques = []
    with open(quesfile) as infile:
        for line in infile:
            top_50_ques.append(line.strip())
    top_50_ques = set(top_50_ques)


    sent_ques = defaultdict(list)
    # {original sentence: list of questions}

    # prev_sent = ''
    with open(logFile) as infile:
        for line in infile:
            if 'INFO ORIGINAL' in line:
                cur_sent = line[line.rindex('INFO ORIGINAL') + len('INFO ORIGINAL'):].strip()
                # if cur_sent[0].islower():
                #     cur_sent = ''
            elif len(cur_sent) != 0:
                quesion = line.split('\t')[1].strip()
                if quesion in top_50_ques:
                    sent_ques[cur_sent].append(quesion)

    # show(sent_ques)

    # Init classes
    article = Article(inputFilePath)
    se = SearchEngine(article)

    count = 0
    count_right = 0

    outfile = codecs.open("eval_SE/test_show_map_top100_unicode_error.txt", "w", "utf-8")


    for ori_sent, ques_list in sent_ques.items():
        print 'ORIGINAL', ori_sent
        outfile.write('ORIGINAL ' + ori_sent + '\n')
        for ques in ques_list:
            result = se.rankByIndri(ques)
            firstSentence = se.returnTopKResult(result, 1)[0].strip()
            print '\tQUE', ques
            outfile.write('\tQUE ' + ques + '\n')
            try:
                print '\t\tRETRIEVED', firstSentence
                # count += 1
                # if ori_sent.lower() in firstSentence.lower():
                #     count_right += 1
                #     print '\t\tMATCH-YES'
                # else:
                #     print '\t\tMATCH-NO'
            except:
                outfile.write('\t\tRETRIEVED ' + firstSentence + '\n')
                if ori_sent.lower() in firstSentence.lower():
                    outfile.write('\t\tMATCH-YES' + '\n')
                else:
                    outfile.write('\t\tMATCH-NO' + '\n')

            # if count % 100 == 0:
            #     print 'Count: %d, right count: %d' % (count, count_right)
            #     print 'Accuracy:', count_right * 1.0 / count







if __name__ == "__main__":
    go('eval_SE/ques-Berlin.txt', 'eval_SE/log-Berlin.txt', 'S10/article/Berlin.txt')


