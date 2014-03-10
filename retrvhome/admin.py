from django.contrib import admin

from retrvhome.models import *

# Register your models here.
class PatentFieldAdmin(admin.ModelAdmin):
	list_display = ('id', 'field_name', 'field_label', 'display', 'retrieve', 'sort')

admin.site.register(PatentField, PatentFieldAdmin)
