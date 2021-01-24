from django.contrib import admin
from .models import Location, Company, Product

# Register your models here.
admin.site.register(Location)
admin.site.register(Product)


def update_location(modeladmin, request, queryset):
    for company in queryset:
        company.location = Location.objects.get(pk=company.unique_id+'0')
        company.save()
update_location.short_description = "Update locations of the companies"


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
    actions =[update_location]

admin.site.register(Company, CompanyAdmin)
