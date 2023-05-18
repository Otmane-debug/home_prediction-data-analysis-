from django.contrib import admin
from .models import House
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class HouseResource(resources.ModelResource):
    class Meta:
        model = House

class HouseAdmin(ImportExportModelAdmin):
    ressource_class = HouseResource


admin.site.register(House,HouseAdmin)