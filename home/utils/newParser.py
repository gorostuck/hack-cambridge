import json
import ast
import sys
import re
import os

cwd = os.path.dirname(os.path.abspath(__file__))
path_to_json = os.path.join(cwd, './sources/scrapes.json') #just change this to the path to the json

with open(path_to_json) as json_file:
    data = json.load(json_file)

ls = ast.literal_eval(data)
company_data, review_data, type_data, location_data, r_photo_data = [], [], [], [], []
all_objects = ls['scrape']

def create_companies():
    for biz in all_objects:
        company = {}
        company['model'] = 'home.company'
        company['pk'] = biz['place_id']
        fields = {}
        fields['location'] = biz['place_id'] + '0'
        fields['name'] = biz['name']
        fields['bio'] = None
        fields['underrep_tag'] = biz['underrep_tag']
        fields['photo_url'] = biz['photoURL']
        fields['num_ratings'] = biz['user_ratings_total']
        fields['rating'] = biz['rating']
        fields['karma'] = None
        fields['gmaps_url'] = biz['googleMapsURL']
        fields['website_url'] = biz['externalWebsiteURL']
        fields['phone'] = biz['phone'].replace(' ', '')
        company['fields'] = fields
        company_data.append(company)

def create_reviews():
    for biz in all_objects:
        for content in biz['reviews']:
            review = {}
            review['model'] = 'home.review'
            fields = {}
            fields['company'] = biz['place_id']
            fields['content'] = content
            review['fields'] = fields
            review_data.append(review)

def create_locations():
    for biz in all_objects:
        location = {}
        location['model'] = 'home.location'
        location['pk'] = biz['place_id'] + '0'
        fields = {}
        fields['address'] = biz['address']
        fields['coord_x'] = biz['location']['lat']
        fields['coord_y'] = biz['location']['lng']
        location['fields'] = fields
        location_data.append(location)

def create_types():
    for biz in all_objects:
        for content in biz['types']:
            types = {}
            types['model'] = 'home.type'
            fields = {}
            fields['company'] = biz['place_id']
            fields['content'] = content
            types['fields'] = fields
            type_data.append(types)

def create_review_photos():
    for biz in all_objects:
        for content in biz['reviewPhotos']:
            r_photos = {}
            r_photos['model'] = 'home.ReviewPhoto'
            fields = {}
            fields['company'] = biz['place_id']
            fields['content'] = content
            r_photos['fields'] = fields
            r_photo_data.append(r_photos)

create_companies()
create_reviews()
create_locations()
create_types()
create_review_photos()

# printing
models = ['company', 'location', 'review', 'type', 'review_photo']
data = [company_data, location_data, review_data, type_data, r_photo_data]
for model, d in zip(models, data):
    dest_f = os.path.join(cwd, '../Fixtures/', str(model) + '.json')
    with open(dest_f, 'w') as outfile:
        json.dump(d, outfile)