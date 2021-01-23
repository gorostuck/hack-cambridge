from django.shortcuts import render
import random
import json


# from .models import Company, Location, Product


# Create your views here.
from home.models import Company, Location


def index(request):
    pass
    # return render(request, 'query.html', context)


def query(request, keyword, location):
    context = {}
    context['keyword']: keyword
    context['location']: location
    '''
    coords = Location.coordinates(location)

    # Returns companies that are close
    nearby = Company.objects.nearby(coords, limit=5)
    context['companies'] = nearby
    '''
    context['companies'] = Company.objects.all()

    return render(request, 'query.html', context)

