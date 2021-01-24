import sys
import re
import json
import os

# open file
cwd = os.path.dirname(os.path.abspath(__file__))
source_f = os.path.join(cwd, './sources/finalScrape.json')
with open(source_f) as f:
    dirty = f.readline()
    clean = re.sub("\\{2}", "", dirty)
    clean = re.sub(r"\\", "", clean)[2:-2].split('}, {') # cleaning

# formatting
for i, j in enumerate(clean):
    if i == 0:
        clean[i] = '%s}' % j
    elif i == len(clean) - 1:
        clean[i] = '{%s' % j
    else:
        clean[i] = '{%s}'% j

company_data, review_data, type_data, location_data = [], [], [], []
for j in clean:
    dummy_json = json.loads(j)

    # set reviews
    for r in dummy_json['reviews']:
        review = {
            'model': 'home.review',
            'fields': {
                'company': dummy_json['place_id'],
                'content': r
            }
        }
        review_data.append(review)

    # set types
    for t in dummy_json['types']:
        type = {
            'model': 'home.type',
            'fields': {
                'company': dummy_json['place_id'],
                'content': t
            }
        }
        type_data.append(type)

    # set companies
    company = {
        'model': 'home.company',
        'pk': dummy_json['place_id'],
        'fields': {
            'location': dummy_json['place_id'] + '0',
            'product': None, #TODO: Assign FK for Product,
            'name': dummy_json['name'],
            'bio': None,
            'underrep_tag': dummy_json['underrep_tag'],
            'photo_url': dummy_json['photoURL'],
            'num_ratings': dummy_json['user_ratings_total'],
            'rating': dummy_json['rating'],
            'karma': None
        }
    }
    company_data.append(company)

    # set locations
    location = {
        'model': 'home.location',
        'pk': dummy_json['place_id'] + '0',
        'fields': {
            'coord_x': dummy_json['location']['lat'],
            'coord_y': dummy_json['location']['lng']
        }
    }
    location_data.append(location)

# printing
models = ['company', 'location', 'review', 'type']
data = [company_data, location_data, review_data, type_data]
for model, d in zip(models, data):
    dest_f = os.path.join(cwd, '../Fixtures/', str(model) + '.json')
    with open(dest_f, 'w') as outfile:
        json.dump(d, outfile)
