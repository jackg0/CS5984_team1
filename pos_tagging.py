import json
import nltk
import string
from nltk.corpus import stopwords
from textblob import TextBlob

with open('archive_spark_hurricane_output.json') as file:
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
