from bs4 import BeautifulSoup
import nltk.data


class Article:
    """Article class parse and stores contents of a single html file

    Attributes:
        filePath: file path
        title: title of this file
        rawLines: list of sentences, each item in the list is one sentence
    """
    def __init__(self, htmlFileName):
        '''
        Parse the html document content to sentences

        :param htmlFileName: path of html file to be parsed
        '''
        with open(htmlFileName) as file:
            self.filePath = htmlFileName
            html_doc = file.read()
            soup = BeautifulSoup(html_doc, "lxml")
            self.title = soup.title.string

            # get contents from the html without section titles
            # ignoring tags like <h1> <h2>
            paragraphs = []
            for paragraph in soup.find_all('p'):
                paragraphs.append(paragraph.get_text())
            data = "\n".join(paragraphs)

            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
            self.rawLines = tokenizer.tokenize(data)



    def showRawLines(self):
        print '\n-----\n'.join(self.rawLines)


    def getTitle(self):
        return self.title


    def getRawLines(self):
        return self.rawLines





if __name__ == '__main__':
    article = Article("data/a1.htm")
    print "=== Title ===\n", article.title
    article.showRawLines()

