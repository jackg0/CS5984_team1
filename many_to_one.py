'''
Converts the big_sample_solr.json file to a .json file with a single dummy
URL and all of the sentences concatenated.

By: Jack Geissinger
'''

import re, time, json
from collections import *
import matplotlib.pyplot as plt
import numpy as np



t0 = time.time()

'''
Load in small dataset and grab sentences
'''
with open('archive_spark_hurricane_output.json') as file:
    data = json.load(file)

noise = ("STAAR", "Getty", "People", "Photo:", "More:", "Subscribe", "SUBSCRIBE",
    "SHARE", "Tags", "RELATED:", "MORE:", "100-year floodplain", "Image", "Salvation", "my", "My")
sentences_list = ['' if any([term in articles['Sentences'] for term in noise])
    else articles['Sentences'] for articles in data]

sentences_list = sentences_list[:len(sentences_list)]
sentences = (' ').join(sentences_list)

output = {}
output["URL"] = "storyblahblah"
output["Sentences_t"] = sentences
with open('small_data.json', 'w') as outfile:
    json.dump(output, outfile)
