from django.shortcuts import render
import random
import json


# Create your views here.
def index(request):
    names = ("bob", "dan", "jack", "lizzy", "susan")

    items = []
    for i in range(5):
        items.append({
            "name": random.choice(names),
            "age": random.randint(20, 80),
            "url": "https://example.com",
        })

    context = {}
    context["items"] = items
    context["items_json"] = json.dumps(items)
    return render(request, 'index.html', context)
