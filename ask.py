from __future__ import division, unicode_literals
import nltk
from nltk.parse.stanford import StanfordParser
import requests
import Helper
from pattern.en import conjugate, lemma, tag
import re
import sys
from Article import Article

reload(sys)
sys.setdefaultencoding('utf-8')

APPOSITION = "NP !< CC !< CONJP < (NP=np1 $.. (/,/ $.. (NP=app $.. /,/)))"
VERB_MODIFIER = "NP=noun > NP $.. VP=modifier"
NP_VP = "S < (NP=np $.. VP=vp)"
verb_tense_dict = {"VBD": "p", "VBP": "1sg", "VBZ": "3sg"}

"""
Remaining work:
- add unmovable mark
- add more rules
- check plural
- coreference resolution
- VBN, VBG check

stanford pos treebank
https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
"""


def getParserTree(line):
    '''
    return parse tree of the string
    :param line: string
    :return: list of tree nodes
    '''
    return list(parser.raw_parse(line))


def getCandidateSentence(text, pattern):
    url = "http://localhost:9000/tregex"
    #request_params = {"pattern": "NP=np < (NP=np1 $.. (/,/ $.. NP=app))"}
    request_params = {"pattern": pattern}
    r = requests.post(url, data=text, params=request_params)
    js = r.json()
    if js['sentences'][0] and '0' in js['sentences'][0] and 'namedNodes' in js['sentences'][0]['0']:
        return js['sentences'][0]['0']['namedNodes']
    return None



def generateAppoQues(sent):
    res = getCandidateSentence(sent, APPOSITION)
    if not res:
        return None
    # parse result
    np1, app = {},{}
    for r in res:
        if 'np1' in r:
            np1 = r['np1']
        if 'app' in r:
            app = r['app']
    nouns1 = re.findall(r'(?<= )\w+(?=\))', np1)
    nouns2 = re.findall(r'(?<= )\w+(?=\))', app)
    head_noun_tag = re.findall(r'(?<=\()\w+(?= )',np1)[1]
    # check if plural
    copula = 'are' if is_plural(head_noun_tag) else 'is'
    ques = ' '.join([copula.capitalize(), ' '.join(nouns1), ' '.join(nouns2), '?'])
    print 'APPO',ques
    return ques


def generateVerbModifierQues(sent):
    res = getCandidateSentence(sent, VERB_MODIFIER)
    if not res:
        return None
    # parse result
    noun, modifier = {},{}
    for r in res:
        if 'noun' in r:
            noun = r['noun']
        if 'modifier' in r:
            modifier = r['modifier']
    nouns, head_noun_tag = get_words_and_tags(noun, 'n')
    modifiers, head_verb_tag = get_words_and_tags(modifier, 'v')
    # check if plural
    copula = 'are' if is_plural(head_noun_tag) else 'is'
    ques = ' '.join([copula.capitalize(), ' '.join(nouns), ' '.join(modifiers), '?'])
    print 'VERB_MODIFIER',ques
    return ques


# should add more constrains/preprocessing
def generateNP_VP_ques(sent):
    res = getCandidateSentence(sent, NP_VP)
    if not res:
        return None
    # parse result
    np, vp = {},{}
    for r in res:
        if 'np' in r:
            np = r['np']
        if 'vp' in r:
            vp = r['vp']
    verb, head_verb_tag = get_words_and_tags(vp, 'v')
    subj, head_subj_tag = get_words_and_tags(np, 'n')
    #print 'v',verb,'subj',subj,'tag',head_subj_tag
    # uncapitalize unless the word is a proper noun
    if not head_subj_tag or not head_subj_tag.startswith('NNP'):
        subj[0]=subj[0].lower()
    # check if contains auxiliary
    if has_auxiliary(head_verb_tag, verb):
        ques = ' '.join([verb[0].capitalize(), ' '.join(subj), ' '.join(verb[1:]), '?'])
        print 'NP VP(aux)',ques
        return ques
    else: # if no auxiliary, insert do
        verb[0] = lemma(verb[0])
        #conjugate('do', get_inflection(head_verb)),
        ques = ' '.join([conjugate('do', get_verb_tense(head_verb_tag)).capitalize(), ' '.join(subj), ' '.join(verb), '?'])
        print 'NP VP(no-aux)', ques


# get words and tags
def get_words_and_tags(tree, flag):
    words = re.findall(r'(?<= )\w+(?=\))', tree)
    tags = re.findall(r'(?<=\()\w+(?= )',tree)
    if flag == 'v':
        head = get_head_verb(tags)
    elif flag == 'n':
        head = get_head_noun(tags)
    return (words, head)


# get head noun
def get_head_noun(tags):
    for tag in tags:
        if tag == 'NP': # we are going to find the children under NP
            continue
        if tag.startswith('N'): # find noun
            return tag


# get head verb
def get_head_verb(tags):
    for tag in tags:
        if tag == 'VP': # we are going to find the children under VP
            continue
        return tag


# check if plural
def is_plural(tag):
    return tag.endswith('S')



# check if contains auxiliary
def has_auxiliary(head_verb_tag, verb):
    if head_verb_tag=='MD' or lemma(verb[0]) in ['be','do','have'] and len(verb)>1:
        return True
    return False


def get_verb_tense(verb_tag):
    return verb_tense_dict[verb_tag]


def ask():
    article = Article('data/a1.htm')
    sentences = article.getRawLines()
    # ignore super long sentences (more than 50 words)
    sentences = [s for s in sentences if s.count(' ') < 50]
    for sent in sentences:
        sent = sent.encode('ascii', 'ignore').decode('ascii')
        #print 'sent',sent
        #tree = Helper.getParserTree(sent)
        #print 'tree',tree
        # APPOSITION
        generateAppoQues(sent)
        generateNP_VP_ques(sent)
        generateVerbModifierQues(sent)


ask()

'''
#text = 'Harry Potter, a young boy, is very famous in US'
text = 'Harry Potter is very famous in US'
#text = 'You must eat'
testTree = Helper.getParserTree(text)
#res = getAppositions(testTree)
print 'test tree',testTree
generateNP_VP_ques(testTree)

res = getNP_VPs(testTree)
print 'result',res
# print one by one
if res:
    for c in res:
        print c
'''
