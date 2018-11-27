'''
POS Tagging for a json file.


Author: Jack Geissinger
'''

import json, nltk, string, sys, getopt
from nltk.corpus import stopwords
from textblob import TextBlob


def findPOSTags(json_file):
    with open(json_file) as file:
        data = json.load(file)

    sentences_list = [articles['Sentences'] for articles in data]

    sentences = (' ').join(sentences_list)

    text_file = open("Output.txt", "w")
    text_file.write(sentences)
    text_file.close()

    blob = TextBlob(sentences)

    noun_group = ['NN', 'NNS', 'NNP', 'NNPS']
    nouns = [(noun,tag) for noun,tag in blob.tags if tag in noun_group]

    for noun, tag in nouns[:5]:
        print(noun, tag)

    verb_group = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    verbs = [(v,t) for v,t in blob.tags if t in verb_group]

    for verb, tag in verbs[:5]:
        print(verb, tag)


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
        print ('python pos_tagging.py -f <file>')

        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('python pos_tagging.py -f <file>')
            sys.exit()
        elif opt in ('-f'):
            json_file = arg

    findPOSTags(json_file)
