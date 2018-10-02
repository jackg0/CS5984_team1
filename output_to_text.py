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
