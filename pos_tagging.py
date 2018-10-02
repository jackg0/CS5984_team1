import json
import nltk
import string
from nltk.corpus import stopwords
from textblob import TextBlob

with open('archive_spark_hurricane_output.json') as file:
    data = json.load(file)

sentences_list = [articles['Sentences'] for articles in data]

sentences = (' ').join(sentences_list)

punctuation = ':;?!.,'
translator = sentences.maketrans('', '', string.punctuation)
sentences = sentences.translate(translator)

text_file = open("Output.txt", "w")
text_file.write(sentences)
text_file.close()

blob = TextBlob(sentences)

noun_group = ['NN', 'NNS', 'NNP', 'NNPS']
nouns = [n for n,t in blob.tags if t in noun_group]
print(nouns[:10])

verb_group = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
verbs = [v for v,t in blob.tags if v in verb_group]
print(verbs[:10])
