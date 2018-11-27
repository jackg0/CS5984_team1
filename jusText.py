# -*- coding: utf-8 -*-

import json
import nltk
import string
import justext
import warc
import requests
import threading
import random
from nltk.corpus import stopwords

def process(record):
	response = requests.get(record['WARC-Target-URI'])
	first = True
	if response.text:
		paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
		heading = ""
		body = ""
		for paragraph in paragraphs:
			if first and paragraph.is_heading:
				#words = filter(lambda word: not word in stopword_set, paragraph.text.split())
				#heading = (' ').join(words)
				heading = paragraph.text
				first = False
			elif not paragraph.is_boilerplate and paragraph.class_type == 'good':
				#words = filter(lambda word: not word in stopword_set, paragraph.text.split())
				#body += (' ').join(words)
				body += " " + paragraph.text
		if body != "":
			body = body.replace('"', "---")
			body = body.replace('\n',"")
			#records.append({"URL":record['WARC-Target-URI'], "Title":heading, "Sentences": body})
			file.write(("{\"URL\":\""+ record['WARC-Target-URI']+"\",\"Title\":\""+heading+"\",\"Sentences\":\""+body+"\"").encode('utf-8').strip())
			file.write('\n')

f = warc.open("Hurricane_Harvey_big.warc.gz")
stopword_set = set(stopwords.words('english'))
filename = "output.json"
file = open(filename, 'a')
numThreads = 50
count = 0
threads = []
for record in f:
	if count % 50 == 0:
		print count
	if len(threads) < numThreads:
		t = threading.Thread(target = process, args=(record,))
		t.start()
		threads.append(t)
	else:
		for t in threads:
		    if not t.isAlive():
		        # get results from thtead
		        t.handled = True
		        threads.remove(t)

		t = threading.Thread(target = process, args=(record,))
		t.start()
		threads.append(t)
	count+=1

for thread in threads:
    thread.join()
