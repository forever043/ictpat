from django.contrib import admin
from rankmgr.models import *

# Register your models here.
class PatentPackageAdmin(admin.ModelAdmin):
	list_display = ('name', 'submit_date', 'finish_date')
	choise_display = 'name'
class PatentRatingReportAdmin(admin.ModelAdmin):
	list_display = ('package', 'patent', 'rating', 'report', 'finish_date')
	choise_display = 'patent'
class PatentExpertRatingAdmin(admin.ModelAdmin):
	list_display = ('package', 'patent', 'expert', 'rank', 'remark', 'submit_date')
	choise_display = 'expert'
admin.site.register(PatentPackage, PatentPackageAdmin)
admin.site.register(PatentRatingReport, PatentRatingReportAdmin)
admin.site.register(PatentExpertRating, PatentExpertRatingAdmin)
