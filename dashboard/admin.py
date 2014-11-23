from django.contrib import admin
from dashboard.models import *

# Register your models here.
class DashboardConfigAdmin(admin.ModelAdmin):
	list_display = ('pk', 'name', 'value', 'memo')
	choise_display = 'pk'
admin.site.register(DashboardConfig, DashboardConfigAdmin)

class ExpertProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'catalog', 'phone', 'organization', 'research_field')
    choise_display = ('user')
admin.site.register(ExpertProfile, ExpertProfileAdmin)

class ExpertCatalogAdmin(admin.ModelAdmin):
    list_display = ('name',)
    choise_display = ('name')
admin.site.register(ExpertCatalog, ExpertCatalogAdmin)
