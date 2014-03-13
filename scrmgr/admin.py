from django.contrib import admin

from patmgr.models import Department
from scrmgr.models import *

# Register your models here.
class SoftwareCRTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sort')
class SoftwareCRStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sort')
class SoftwareCRAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'developers', 'version', 'reg_code', 'release_date', 'authorize_date', 'authorize_file')

#class SoftwareCRExtFieldTypeAdmin(admin.ModelAdmin):
#    list_display = ('id', 'field_name', 'field_label', 'retrieval', 'disabled', 'sort')
#class SoftwareCRExtFieldAdmin(admin.ModelAdmin):
#    list_display = ('id', 'patent', 'type', 'value')
#class SoftwareCRRankAdmin(admin.ModelAdmin):
#    list_display = ('id', 'expert', 'rank')

admin.site.register(SoftwareCRType, SoftwareCRTypeAdmin)
admin.site.register(SoftwareCRState, SoftwareCRStateAdmin)
admin.site.register(SoftwareCR, SoftwareCRAdmin)
#admin.site.register(SoftwareCRExtFieldType, SoftwareCRExtFieldTypeAdmin)
#admin.site.register(SoftwareCRExtField, SoftwareCRExtFieldAdmin)
#admin.site.register(SoftwareCRRank, SoftwareCRRankAdmin)


#class RetrvSchemeAdmin(admin.ModelAdmin):
#	list_display = ('id', 'name', 'current')
#class BuiltinRetrvFieldAdmin(admin.ModelAdmin):
#	list_display = ('id', 'field_name', 'scheme', 'retrieve', 'display', 'sort')
#class CustomizedRetrvFieldAdmin(admin.ModelAdmin):
#	list_display = ('id', 'field', 'scheme', 'retrieve', 'display', 'sort')
#admin.site.register(RetrvScheme, RetrvSchemeAdmin)
#admin.site.register(BuiltinRetrvField, BuiltinRetrvFieldAdmin)
#admin.site.register(CustomizedRetrvField, CustomizedRetrvFieldAdmin)
