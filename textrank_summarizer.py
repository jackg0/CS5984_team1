import json
from summa import summarizer
import time

t0 = time.time()

with open('archive_spark_hurricane_output.json') as file:
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
print('Extraction summary - time elapsed:', time.time() - t0)
