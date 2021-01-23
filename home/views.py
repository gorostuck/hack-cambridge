from django.shortcuts import render
import random
import json


# from .models import Company, Location, Product


# Create your views here.
def index(request):
    pass
    # return render(request, 'index.html', context)


def query(request, keyword, location):
    context = {}
    context['keyword']: keyword
    context['location']: location
    # coords = Location.coordinates(location)

    '''
    Returns companies that are more 
    nearby = Company.nearby(coords, limit=5)
    
    '''

    return render(request, 'index.html', {'keyword': keyword, 'location': location})
