'''
Hurricane Harvey template summarizer


Author: Jack Geissinger
'''


import spacy, re, time, json, sys, getopt
from collections import *
import matplotlib.pyplot as plt
import numpy as np

def generateTemplateSummary(json_file):
    '''
    Medium sized set works better than small set, which did not
    contain "Category [1-5]".
    '''
    nlp = spacy.load('en_core_web_md')

    t0 = time.time()

    '''
    Load in small dataset and grab sentences
    '''
    with open(json_file) as file:
        data = json.load(file)

    noise = ("STAAR", "Getty", "People", "Photo:", "More:", "Subscribe", "SUBSCRIBE",
        "SHARE", "Tags", "RELATED:", "MORE:", "100-year floodplain", "Image")
    sentences_list = ['' if any([term in articles['Sentences'] for term in noise])
        else articles['Sentences'] for articles in data]

    sentences_list = sentences_list[:len(sentences_list)]
    sentences = (' ').join(sentences_list)

    '''
    Throw sentences into spacy and make a hashmap for all of the named entities
    that are found.
    '''
    doc = nlp(sentences)
    ents = list(doc.ents)
    entsHash = {}

    for ent in ents:
        if ent.label_ not in entsHash:
            entsHash[ent.label_] = OrderedDict()
            entsHash[ent.label_][ent.text] = 1
        else:
            if ent.text not in entsHash[ent.label_]:
                entsHash[ent.label_][ent.text] = 1
            else:
                entsHash[ent.label_][ent.text] += 1
    '''
    Define slots dict to store information
    '''
    slots = {}

    '''
    Define entities expected to be chosen based on most frequently cited,
    and store them in slots.
    '''
    ent_freq = ['EVENT', 'LOC', 'GPE', 'ORG', 'MONEY']

    for ent_type in ent_freq:
        item = max(entsHash[ent_type].items(),
            key = lambda item : item[1])
        slots[ent_type] = item[0]

    '''
    Choose most frequently cited month associated with the event
    '''
    month_abbrev = {'January' : ('January', 'Jan.', 'Jan'),
        'February' : ('February', 'Feb.', 'Feb'), 'March' : ('Mar', 'March'),
        'April' : ('Apr', 'April'), 'May' : ('May','May'),     'June' : ('Jun', 'Jun.', 'June'),
        'July' : ('Jul', 'July'), 'August' : ('August', 'Aug.', 'Aug'),
        'September' : ('September', 'Sept', 'Sept.'), 'October' : ('October', 'Oct', 'Oct.'),
        'November' : ('November', 'Nov', 'Nov.'), 'December' : ('December', 'Dec', 'Dec.')}

    months = defaultdict(int)

    for month in month_abbrev.keys():
        for item in entsHash['DATE'].items():
            if any([term in item[0] for term in month_abbrev[month]]):
                months[month] += item[1]

    months = sorted(months.items(), key = lambda item : item[1], reverse=True)
    slots['MONTH'] = months[0][0]

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
                slots['YEAR'] = year

    '''
    Choose most frequently cited Category 1-5 associated with the event
    '''
    category = defaultdict(int)
    max_count = 0
    for quantity in entsHash['QUANTITY'].items():
        if 'Category' in quantity[0]:
            category[quantity[0]] += quantity[1]
            if category[quantity[0]] > max_count:
                max_count = category[quantity[0]]
                slots['CATEGORY'] = quantity[0]

    '''
    range_quantities(type) will find inches, mph, or other quantities,
    make an array of numbers associated with those quantities,
    bin them using matplotlib, and find a range for the most frequent
    quantities.
    '''
    def range_quantities(type):
        numbers = []
        for quantity in entsHash['QUANTITY'].items():
            if type in quantity[0]:
                number = re.findall(r'\d+', quantity[0])
                if len(number) == 1:
                    numbers += number*quantity[1]
        numbers = [int(number) for number in numbers]
        numbers.sort()

        (n, bins, patches) = plt.hist(numbers, bins='auto')
        idx = np.argmax(n)
        ranges = [int(bins[idx]), int(bins[idx+1])]
        return ranges

    slots['RAINFALL'] = range_quantities('inches')
    slots['WINDSPEED'] = range_quantities('mph')

    '''
    Construct the summary.
    '''
    print("{} was a {} hurricane that made landfall in {}, {} in {}.".format(slots['EVENT'],
        slots['CATEGORY'], slots['MONTH'], slots['YEAR'], slots['GPE']))
    print("The hurricane traveled through {} with windspeeds that ranged from a low of {} mph to a peak of {} mph.".format(slots['LOC'],
        slots['WINDSPEED'][0], slots['WINDSPEED'][1]))
    print("In addition, the rainfall from {} varied in areas, but there seemed to be around {} inches to {} inches in many areas.".format(slots['EVENT'],
        slots['RAINFALL'][0], slots['RAINFALL'][1]))
    print("{} was primarily involved with dealing with the affected area, and {} in damage was caused.".format(slots['ORG'], slots['MONEY']))

    print()
    print("Time elapsed: {}".format(time.time() - t0))


if __name__ == '__main__':

    try:
       opts, args = getopt.getopt(sys.argv[1:],'h:f:')
    except getopt.GetoptError:

        print ('opts:')
        print (opts)

        print ('\n')
        print ('args:')
        print (args)

        print ('Incorrect usage of command line: ')
        print ('python template_summarizer.py -f <file>')

        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('python template_summarizer.py -f <file>')
            sys.exit()
        elif opt in ('-f'):
            json_file = arg

    generateTemplateSummary(json_file)
