from django.urls import path
from home import views

urlpatterns = [
    path('query/<str:keyword>-<str:location>', views.query, name='query'),
]
