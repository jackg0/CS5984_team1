'''
Takes a Wikipedia article and gets the content.

By: Jack Geissinger
'''

import re, time, json, wikipedia, string
from collections import *
import numpy as np

'''
Source: https://stackoverflow.com/questions/37605045/cleaning-wikipedia-content-with-python
'''
def parse(raw_content):
    section_title_re = re.compile("^=+\s+.*\s+=+$")
    content = []
    skip = False
    for l in raw_content.splitlines():
        line = l.strip()
        if "= references =" in line.lower():
            skip = True  # replace with break if this is the last section
            continue
        if "= further reading =" in line.lower():
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
Load in Wikipedia article
'''
page = wikipedia.page("Hurricane Harvey")
text = parse(page.content)

output = {}
output["URL"] = "wikipedia-article"
output["Sentences_t"] = text
with open('wikipedia-article.json', 'w') as outfile:
    json.dump(output, outfile)
