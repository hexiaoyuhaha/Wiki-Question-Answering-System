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
