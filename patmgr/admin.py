from django.contrib import admin
from patmgr.models import Department, PatentType, PatentState, PatentExtFieldType, PatentExtField, PatentRank, Patent

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
