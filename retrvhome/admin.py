from django.contrib import admin

from retrvhome.models import *

# Register your models here.
class PatentFieldAdmin(admin.ModelAdmin):
	list_display = ('id', 'field_name', 'field_label', 'display', 'retrieve', 'type', 'sort')

class RetrvSoftwareCRFieldAdmin(admin.ModelAdmin):
	list_display = ('id', 'field_name', 'field_label', 'display', 'retrieve', 'type', 'sort')

admin.site.register(PatentField, PatentFieldAdmin)
admin.site.register(RetrvSoftwareCRField, RetrvSoftwareCRFieldAdmin)
