from django.contrib import admin
from .models import Location, Company, Product

# Register your models here.
admin.site.register(Location)
admin.site.register(Company)
admin.site.register(Product)