from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('query/<str:keyword>-<str:location>', views.query, name='query'),
    path('landing/<str:pk>', views.landing_page, name='landing'),
    path('landing/<str:pk>/<str:keyword>-<str:location>', views.landing_page, name='landing'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
