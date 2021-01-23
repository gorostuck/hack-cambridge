from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('query/<str:keyword>-<str:location>', views.query, name='query'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
