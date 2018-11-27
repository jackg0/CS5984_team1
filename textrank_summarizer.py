'''
Hurricane Harvey template summarizer


Author: Jack Geissinger
'''


import json, sys, getopt
from summa import summarizer
import time

def generateTextRankSummary(json_file):

    t0 = time.time()

    with open(json_file) as file:
        data = json.load(file)

    noise = ['People', 'Photo:', 'More:', 'Subscribe', 'SUBSCRIBE', 'SHARE', 'Tags', 'RELATED:', 'MORE:', '100-year floodplain', 'Image']
    sentences_list = ['' if any([term in articles['Sentences'] for term in noise]) else articles['Sentences'] for articles in data]

    # Reducing data set size:
    # sentences_list = sentences_list[:len(sentences_list)]
    print('Number of sentences:', len([sentence for sentence in sentences_list if sentence]))
    sentences = (' ').join(sentences_list)

    print('Reading JSON file - time elapsed:', time.time() - t0)

    url = 'All articles'
    text = sentences
    print('----------------------------------')
    t0 = time.time()
    output_sentences = summarizer.summarize(sentences, words=100, scores=True)
    output_sentences = sorted(output_sentences, key=lambda x : x[1], reverse=True)
    for idx, output in enumerate(output_sentences):
        print('Sentence number:', idx, 'Score:', output[1])
        print(output[0])
    print('----------------------------------')
    print('Summary complete - time elapsed:', time.time() - t0)

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
        print ('python textrank_summarizer.py -f <file>')

        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('python textrank_summarizer.py -f <file>')
            sys.exit()
        elif opt in ('-f'):
            json_file = arg

    generateTextRankSummary(json_file)
