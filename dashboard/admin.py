from django.contrib import admin
from dashboard.models import *

# Register your models here.
class DashboardConfigAdmin(admin.ModelAdmin):
	list_display = ('pk', 'name', 'value', 'memo')
	choise_display = 'pk'
admin.site.register(DashboardConfig, DashboardConfigAdmin)

class ExpertProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'organization', 'research_field')
    choise_display = ('user')
admin.site.register(ExpertProfile, ExpertProfileAdmin)

#class ExpertProfileInline(admin.StackedInline):
#    model = ExpertProfile
 #   max_num = 1
#    can_delete = False
#class ExpertUserAdmin(UserAdmin):
#    inlines = [ExpertProfileInline,]
#admin.site.unregister(User)
#admin.site.register(User, ExpertUserAdmin)
