from bs4 import BeautifulSoup
import nltk.data


class Article:
    """Article class parse and stores contents of a single html file

    Attributes:
        filePath: file path
        title: title of this file
        rawLines: list of sentences, each item in the list is one sentence
    """
    def __init__(self, fileName):
        '''
        Parse the html document content to sentences

        :param htmlFileName: path of html file to be parsed
        '''
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        if fileName.endswith('.htm'):
            with open(fileName) as file:
                self.filePath = fileName
                html_doc = file.read()
                soup = BeautifulSoup(html_doc, "lxml")
                self.title = soup.title.string

                # get contents from the html without section titles
                # ignoring tags like <h1> <h2>
                paragraphs = []
                for paragraph in soup.find_all('p'):
                    paragraphs.append(paragraph.get_text())
                data = "\n".join(paragraphs)
                self.rawLines = tokenizer.tokenize(data)
        elif fileName.endswith('.txt'):
            with open(fileName) as file:
                self.filePath = fileName
                self.title = file.readline()
                lines = file.readlines()
                lines = [line.strip() for line in lines if line]
                # doc = ' '.join(lines)
                self.rawLines = []
                for line in lines:
                    self.rawLines += tokenizer.tokenize(line.decode('utf-8'))
        else:
            print 'Error, unable to read file', fileName


    def showRawLines(self):
        print u'\n-----\n'.join(self.rawLines).encode('utf-8').strip()


    def getTitle(self):
        return self.title


    def getRawLines(self):
        return self.rawLines


if __name__ == '__main__':
    # article = Article("data/a1.htm")
    article = Article("data/a1.txt")
    print "=== Title ===\n", article.title
    article.showRawLines()
