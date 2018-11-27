'''
Takes a Wikipedia article and gets the content.

By Jack Geissinger
'''

import re, time, json, wikipedia, string, sys, getopt, hashlib
from collections import *
from subprocess import call

'''
Parse content of Wikipedia file
Source: https://stackoverflow.com/questions/37605045/cleaning-wikipedia-content-with-python
'''
def parseContent(raw_content):
    section_title_re = re.compile('^=+\s+.*\s+=+$')
    content = []
    skip = False
    for l in raw_content.splitlines():
        line = l.strip()
        if '= references =' in line.lower():
            skip = True  # replace with break if this is the last section
            continue
        if '= further reading =' in line.lower():
            skip = True  # replace with break if this is the last section
            continue
        if section_title_re.match(line):
            skip = False
            continue
        if skip:
            continue
        content.append(line)

    content = '\n'.join(content) + '\n'
    content = content.replace('\n', '')
    printable = set(string.printable)
    content = filter(lambda x: x in printable, content)
    return content

'''
Write to story file.
'''
def writeStory(sentences, name):
    fileName = 'tmp/' + name + '.story' #create the. story file version of the article
    FILE = open(fileName,'w')
    FILE.write(sentences)
    FILE.close()

    URL_FILE = open('all_urls.txt','w')
    URL_FILE.write(name + '\n')
    URL_FILE.close()

'''
Returns a heximal formated SHA1 hash of the input string.
'''
def hashhex(s):
  h = hashlib.sha1()
  h.update(s)
  return h.hexdigest()

'''
Load in Wikipedia article
'''
def loadContent(topic, outputDir):
    page = wikipedia.page(topic)
    content = parseContent(page.content)
    name = hashhex(topic)
    writeStory(content, name)


if __name__ == '__main__':

    print (sys.argv)
    print

    try:
       opts, args = getopt.getopt(sys.argv[1:],'t:h:o:')
    except getopt.GetoptError:

        print ('opts:')
        print (opts)

        print ('\n')
        print ('args:')
        print (args)

        print ('Incorrect usage of command line: ')
        print ('python wikipedia_content.py -t <topic> -o <output directory>')



        sys.exit(2)

    #initialize cmd line variables with default calues
    topic = None
    outputDir = None


    for opt, arg in opts:
        print (opt,'\t',arg)
        if opt == '-h':
            print ('python wikipedia_content.py -t <topic> -o <output directory>')
            sys.exit()
        elif opt in ('-t'):
            topic = arg
        elif opt in ('-o'):
            outputDir = arg


    print('\n')
    print('Topic:', topic)
    print('Output directory:', outputDir)
    print('\n')

    loadContent(topic,outputDir)
    call(['python', 'make_datafiles.py', './tmp', 'test.bin'])
