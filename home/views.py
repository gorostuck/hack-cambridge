from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Create your views here.
from home.forms import SearchForm
from home.models import Company, Location


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            keyword = form.cleaned_data['keyword']
            location = form.cleaned_data['location']
            # redirect to a new URL:
            url = '/query/'+keyword+'-'+location
            return HttpResponseRedirect(url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'index.html', {'form': form})


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
    user_loc = Location.objects.create(post_code=location)
    context['companies'] = Company.objects.nearby(
        coords=[user_loc.coord_x, user_loc.coord_y], limit=3)
    #print(context['companies'])
    user_loc.delete()

    return render(request, 'query.html', context)

