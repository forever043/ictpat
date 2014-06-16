from django.contrib import admin
from patmgr.models import *

# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    choise_display = 'name'
class PatentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sort')
class PatentStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sort')
class PatentExtFieldTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'field_name', 'field_label', 'retrieval', 'disabled', 'sort')
class PatentExtFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'patent', 'type', 'value')
class PatentRankAdmin(admin.ModelAdmin):
    list_display = ('id', 'expert', 'rank')
class PatentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state')

admin.site.register(Department, DepartmentAdmin)
admin.site.register(PatentType, PatentTypeAdmin)
admin.site.register(PatentState, PatentStateAdmin)
admin.site.register(PatentExtFieldType, PatentExtFieldTypeAdmin)
admin.site.register(PatentExtField, PatentExtFieldAdmin)
admin.site.register(PatentRank, PatentRankAdmin)
admin.site.register(Patent, PatentAdmin)


class RetrvSchemeAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'current')
class BuiltinRetrvFieldAdmin(admin.ModelAdmin):
	list_display = ('id', 'field_name', 'scheme', 'retrieve', 'type', 'display', 'sort')
class CustomizedRetrvFieldAdmin(admin.ModelAdmin):
	list_display = ('id', 'field', 'scheme', 'retrieve', 'type', 'display', 'sort')
admin.site.register(RetrvScheme, RetrvSchemeAdmin)
admin.site.register(BuiltinRetrvField, BuiltinRetrvFieldAdmin)
admin.site.register(CustomizedRetrvField, CustomizedRetrvFieldAdmin)
