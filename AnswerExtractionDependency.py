import spacy
nlp = spacy.load('en')




if __name__ == '__main__':
    text = u'Bullet ants are located in Central and South America.'
    doc = nlp(text)
