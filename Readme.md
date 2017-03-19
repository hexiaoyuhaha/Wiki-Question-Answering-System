# AT_detection.py (by Jiong, March 19)
This py file will take a sentence question as input and ouptut a answer type classified by SVM. The training set and test set are AT_train.txt and AT_test.txt. Also as the pos tagging and ner process takes a long time, all the feature data are uploaded to the repository.

** Remaining Work **
Try more features on it.

# Helper.py (by Shuang, March 30)
Helper.py assume you have following packages:
- nltk (include some basic corpus like stopwords)
- textblob
- StanfordPOSTagger
- StanfordNERTagger
- StanfordParser
- StanfordDependencyParser

**Some questions for further discussion:**
- text preprocessing:
    - when do we remove stopwords
    - when do we use lower case
    - when do we use stem word
    - I can create more methods to efficiently deal with preprocessing without n-pass loop:
      - eg. remove stop words and do stemming in one pass; remove stop words before tfidf calculation


# Article.py (by Xiaoyu, March 12)
Article class parse and stores contents of a single html file.

Article.py assume you have following packages:
- nltk.data, 'tokenizers/punkt/english.pickle'
- BeautifulSoup

**Remaining Work**
- Parser the html file and extract the section title, retain the relationship between section name and its content
    - self.sections  {Key: subtitle, Value: string}
    - dict getSection()


# SearchEngine.py (by Xiaoyu, March 12)
SearchEngine class finds the best match sentences using given document and query

**Note:**
- input query should be a list and removed stop words

**Remaining work:**
    - Implement `getDocScore` methods.
    - Add LeToR SVM ranking to improve ranking accuracy
    - Adding advanced functionality to use sections titles improve accuracy
