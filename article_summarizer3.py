import spacy
import requests, re
import time
import json
from collections import *
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

nlp = spacy.load('en_core_web_md')

t0 = time.time()

'''
Load in small dataset and grab sentences
'''
with open('archive_spark_hurricane_output.json') as file:
    data = json.load(file)

noise = ("STAAR", "Getty", "People", "Photo:", "More:", "Subscribe", "SUBSCRIBE", "SHARE", "Tags", "RELATED:", "MORE:", "100-year floodplain", "Image")
sentences_list = ['' if any([term in articles['Sentences'] for term in noise]) else articles['Sentences'] for articles in data]

sentences_list = sentences_list[:len(sentences_list)]
sentences = (' ').join(sentences_list)

'''
Import URLs for extra text to add into the mix.
'''
# source: https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
def url_to_string(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html5lib')
    for script in soup(['script', 'style', 'aside']):
        script.extract()
    return ' '.join(re.split(r'[\n\t]+', soup.get_text()))

cnn_sentences = url_to_string('https://www.cnn.com/specials/us/hurricane-harvey')

sentences = sentences + ' ' + cnn_sentences


'''
Throw sentences into spacy and make a hashmap for all of the named entities
that are found.
'''
doc = nlp(sentences)
ents = list(doc.ents)
entsHash = {}

for ent in ents:
    if ent.label_ not in entsHash:
        entsHash[ent.label_] = {}
        entsHash[ent.label_][ent.text] = 1
    else:
        if ent.text not in entsHash[ent.label_]:
            entsHash[ent.label_][ent.text] = 1
        else:
            entsHash[ent.label_][ent.text] += 1

'''
Choose most frequent event, which will correspond to the hurricane we are studying
'''
events = sorted(entsHash['EVENT'].items(), key = lambda item : item[1], reverse=True)
main_event = events[0][0]

'''
Choose most frequent location for where it traveled, and most common ocean for where it originated
'''
locations = sorted(entsHash['LOC'].items(), key = lambda item : item[1], reverse=True)
main_loc = locations[0][0]

oceans = ['Atlantic', 'Pacific', 'Arctic', 'Indian', 'Southern']
for loc in locations:
    if any([ocean in loc[0][0] for ocean in oceans]):
        ocean = loc[0][0]
        break

'''
Choose most frequently cited city or state related to the event
'''
cities_states = sorted(entsHash['GPE'].items(), key = lambda item : item[1], reverse=True)
main_city_state = cities_states[0][0]

'''
Choose organization most involved with the event
'''
orgs = sorted(entsHash['ORG'].items(), key = lambda item : item[1], reverse=True)
main_org = orgs[0][0]

'''
Choose most frequently cited cost associated with the event
'''
damages = sorted(entsHash['MONEY'].items(), key = lambda item : item[1], reverse=True)
main_damage = damages[0][0]

'''
Choose most frequently cited month associated with the event
'''
month_abbrev = {'January' : ('January', 'Jan.', 'Jan'), 'February' : ('February', 'Feb.', 'Feb'), 'March' : ('Mar', 'March'), 'April' : ('Apr', 'April'),
    'May' : ('May','May'), 'June' : ('Jun', 'Jun.', 'June'), 'July' : ('Jul', 'July'), 'August' : ('August', 'Aug.', 'Aug'), 'September' : ('September', 'Sept', 'Sept.'),
    'October' : ('October', 'Oct', 'Oct.'), 'November' : ('November', 'Nov', 'Nov.'), 'December' : ('December', 'Dec', 'Dec.')}
months = defaultdict(int)

for month in month_abbrev.keys():
    for item in entsHash['DATE'].items():
        if any([term in item[0] for term in month_abbrev[month]]):
            months[month] += item[1]

months = sorted(months.items(), key = lambda item : item[1], reverse=True)
main_month = months[0][0]

'''
Choose most frequently cited year associated with the event
'''
years = defaultdict(int)
max_count = 0
for item in entsHash['DATE'].items():
    year = re.findall(r'\d{4}', item[0])
    if len(year) == 1:
        year = year[0]
        years[year] += 1
        if years[year] > max_count:
            max_count = years[year]
            main_year = year

'''
Evaluate inches of rainfall and then place rainfall in bins with
matplotlib and report the bin edges with the most frequency.
'''
inches = []
for quantity in entsHash['QUANTITY'].items():
    if 'inches' in quantity[0]:
        numbers = re.findall(r'\d+',quantity[0])
        if len(numbers) == 1:
            inches += numbers*quantity[1]

inches = [int(inch) for inch in inches]
inches.sort()

(n, bins, patches) = plt.hist(inches, bins='auto')
idx = np.argmax(n)
rainfall_range = [int(bins[idx]), int(bins[idx+1])]

'''
Evaluate the windspeed of the Hurricane and determine most frequent range
of windspeeds if binned by matplotlib.
'''
windspeeds = []
for quantity in entsHash['QUANTITY'].items():
    if 'mph' in quantity[0]:
        numbers = re.findall(r'\d+', quantity[0])
        if len(numbers) == 1:
            windspeeds += numbers*quantity[1]

windspeeds = [int(windspeed) for windspeed in windspeeds]
windspeeds.sort()

(n, bins, patches) = plt.hist(windspeeds, bins='auto')
idx = np.argmax(n)
windspeed_range = [int(bins[idx]), int(bins[idx+1])]

'''
Find most frequent mention of Category in QUANTITY
'''
category = defaultdict(int)
max_count = 0
for quantity in entsHash['QUANTITY'].items():
    if 'Category' in quantity[0]:
        category[quantity[0]] += quantity[1]
        if category[quantity[0]] > max_count:
            max_count = category[quantity[0]]
            main_category = quantity[0]

print("{} was a {} hurricane that made landfall on {}, {} in {}.".format(main_event, main_category, main_month, main_year, main_city_state))
print("The hurricane traveled through {} with windspeeds that ranged from a low of {} mph to a peak of {} mph.".format(main_loc, windspeed_range[0], windspeed_range[1]))
print("In addition, the rainfall from {} varied in areas, but there seemed to be around {} inches to {} inches in many areas.".format(main_event, rainfall_range[0], rainfall_range[1]))
print("{} was primarily involved with dealing with the affected area, and {} in damage was caused.".format(main_org, main_damage))


print(sorted(entsHash['LOC'].items(), key = lambda item : item[1], reverse=True))

print("Time elapsed: {}".format(time.time() - t0))
