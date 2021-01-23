import sys
import re
import json

# open file
source_f = sys.argv[1]
with open(source_f) as f:
    dirty = f.readline()
    clean = re.sub(r"\\", "", dirty)[2:-2].split('}, {') # cleaning

# formatting
for i, j in enumerate(clean):
    if i == 0:
        clean[i] = '%s}' % j
    elif i == len(clean) - 1:
        clean[i] = '{%s' % j
    else:
        clean[i] = '{%s}' % j

# parsing
company_data, location_data = [], []
for j in clean:
    dummy_json = json.loads(j)

    company = {
        'model': 'home.company',
        'pk': dummy_json['place_id'],
        'fields': {
            'name': dummy_json['name'],
            'bio': None,
        }
    }
    company_data.append(company)

    location = {
        'model': 'home.location',
        'unique_id': dummy_json['place_id'] + '0',
        'fields': {
            'coord_x': dummy_json['location']['lat'],
            'coord_y': dummy_json['location']['lng']
        }
    }
    location_data.append(location)

# printing
models = ['company', 'location']
data = [company_data, location_data]
for model, d in zip(models, data):
    dest_f = sys.argv[2] + str(model) + '.json'
    with open(dest_f, 'a') as outfile:
        json.dump(d, outfile)
