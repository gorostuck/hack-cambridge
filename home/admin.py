from django.contrib import admin
from .models import Location, Company, Product, Review, Type

# Register your models here.
admin.site.register(Location)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Type)


def update_location(modeladmin, request, queryset):
    for company in queryset:
        company.location = Location.objects.get(pk=company.unique_id + '0')
        company.save()


update_location.short_description = "Update locations of the companies"


def remove_duplicate_tags(modeladmin, request, queryset):
    for company in queryset:
        company_types = company.type_set.all()
        remain = []
        for type in company_types:
            if type.content not in remain:
                remain.append(type.content)
            else:
                type.delete()
remove_duplicate_tags.short_description = "Remove duplicate tags"


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_x_coord', 'get_y_coord']

    def get_x_coord(self, obj):
        return obj.location.coord_x

    def get_y_coord(self, obj):
        return obj.location.coord_y

    actions = [update_location, remove_duplicate_tags]


admin.site.register(Company, CompanyAdmin)
