from django.contrib import admin
from dashboard.models import *

# Register your models here.
class DashboardConfigAdmin(admin.ModelAdmin):
	list_display = ('pk', 'name', 'value', 'memo')
	choise_display = 'pk'
admin.site.register(DashboardConfig, DashboardConfigAdmin)

