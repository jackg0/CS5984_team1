"""
Edmunson and LSA Extractive Summarizers using the sumy library
Source/Tutorial: http://ai.intelligentonlinetools.com/ml/text-summarization/
Author: Jack
"""

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import json
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
import time
from nltk.corpus import stopwords

SENTENCES_COUNT = 5
LANGUAGE = "english"

t0 = time.time()

with open('archive_spark_hurricane_output.json') as file:
    data = json.load(file)

noise = ("STAAR", "Getty", "People", "Photo:", "More:", "Subscribe", "SUBSCRIBE", "SHARE", "Tags", "RELATED:", "MORE:", '100-year floodplain', 'Image')
sentences_list = ['' if any([term in articles['Sentences'] for term in noise]) else articles['Sentences'] for articles in data]

sentences_list = sentences_list[:len(sentences_list)]
sentences = (' ').join(sentences_list)

parser = PlaintextParser.from_string(sentences, Tokenizer(LANGUAGE))

print("Reading JSON file - time elapsed:", time.time() - t0)

print('---------------------------------')
print('-------EdmundsonSummarizer-------')
t0 = time.time()

summarizer = EdmundsonSummarizer()

bonus_words = ("Harvey", "Houston")
summarizer.bonus_words = bonus_words

noise = ("Tag", "Getty", "People", "Photo:", "More:", "Subscribe", "SUBSCRIBE", "SHARE", "Tags", "RELATED:", "MORE:", '100-year floodplain', 'Image')
summarizer.stigma_words = noise
summarizer.null_words = noise

for sentence in summarizer(parser.document, SENTENCES_COUNT):
    print(sentence)
print('---------------------------------')
print("Extraction summary - time elapsed:", time.time() - t0)


print('---------------------------------')
print('----------LsaSummarizer----------')
t0 = time.time()
summarizer = LsaSummarizer()
summarizer = LsaSummarizer(Stemmer(LANGUAGE))
stopword_set = set(stopwords.words(LANGUAGE))
summarizer.stop_words = stopword_set
for sentence in summarizer(parser.document, SENTENCES_COUNT):
    print(sentence)
print('---------------------------------')
print("Extraction summary - time elapsed:", time.time() - t0)
