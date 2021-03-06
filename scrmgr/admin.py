from django.contrib import admin

from patmgr.models import Department
from scrmgr.models import *

# Register your models here.
class SoftwareCRAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'developers', 'release_date', 'version', 'authorize_code', 'authorize_date', 'authorize_file')

class SoftwareCRExtFieldTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'field_name', 'field_label', 'retrieval', 'disabled', 'sort')
class SoftwareCRExtFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'scr', 'type', 'value')
#class SoftwareCRRankAdmin(admin.ModelAdmin):
#    list_display = ('id', 'expert', 'rank')

admin.site.register(SoftwareCR, SoftwareCRAdmin)
admin.site.register(SoftwareCRExtFieldType, SoftwareCRExtFieldTypeAdmin)
admin.site.register(SoftwareCRExtField, SoftwareCRExtFieldAdmin)
#admin.site.register(SoftwareCRRank, SoftwareCRRankAdmin)


class RetrvSchemeAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'current')
class BuiltinRetrvFieldAdmin(admin.ModelAdmin):
	list_display = ('id', 'field_name', 'scheme', 'retrieve', 'type', 'display', 'sort')
class CustomizedRetrvFieldAdmin(admin.ModelAdmin):
	list_display = ('id', 'field', 'scheme', 'retrieve', 'type', 'display', 'sort')
admin.site.register(RetrvScheme, RetrvSchemeAdmin)
admin.site.register(BuiltinRetrvField, BuiltinRetrvFieldAdmin)
admin.site.register(CustomizedRetrvField, CustomizedRetrvFieldAdmin)
