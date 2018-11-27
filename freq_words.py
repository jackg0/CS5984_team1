'''
Most frequent words for a json file.

Author: Jack Geissinger
'''
import json, nltk, string, sys, getopt
from nltk.corpus import stopwords

def findFreqWords(json_file):
    with open(json_file) as file:
        data = json.load(file)

    noise = ["Photo:", "More:", "Subscribe", "SUBSCRIBE", "SHARE", "Tags", "RELATED:", "MORE:", '100-year floodplain', 'Image']
    sentences_list = ['' if any([term in articles['Sentences'] for term in noise]) else articles['Sentences'] for articles in data]

    sentences = (' ').join(sentences_list)

    sentences = sentences.lower()
    punctuation = ':;?!.,'
    translator = sentences.maketrans('', '', punctuation)
    sentences = sentences.translate(translator)

    stopword_set = set(stopwords.words('english'))
    words = filter(lambda word: not word in stopword_set, sentences.split())

    freqDist = nltk.FreqDist(words)

    mostFreqWords = freqDist.most_common(5)

    for word, count in mostFreqWords:
        print(word, count)


if __name__ == '__main__':

    try:
       opts, args = getopt.getopt(sys.argv[1:],'h:f:')
    except getopt.GetoptError:

        print ('opts:')
        print (opts)

        print ('\n')
        print ('args:')
        print (args)

        print ('Incorrect usage of command line: ')
        print ('python freq_words.py -f <file>')

        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('python freq_words.py -f <file>')
            sys.exit()
        elif opt in ('-f'):
            json_file = arg

    findFreqWords(json_file)
