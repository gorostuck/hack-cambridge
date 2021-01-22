from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vuetify', views.alt_index, name='vuetify'),
]
