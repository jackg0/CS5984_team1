'''
author: Jack
'''
import json
import nltk
import string
from nltk.corpus import stopwords

with open('archive_spark_hurricane_output.json') as file:
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

fdist = nltk.FreqDist(words)

print(fdist.most_common(50))
