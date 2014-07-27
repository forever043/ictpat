# -*- coding: UTF-8 -*-
from django.contrib import admin
from rankmgr.models import *

# 专利评价管理
class PatentPackageAdmin(admin.ModelAdmin):
	list_display = ('name', 'rating_weight', 'submit_date', 'finish_date')
	choise_display = 'name'
class PatentRatingReportAdmin(admin.ModelAdmin):
	list_display = ('package', 'patent', 'rating', 'rank', 'report', 'finish_date')
	choise_display = 'patent'
class PatentExpertRatingAdmin(admin.ModelAdmin):
	list_display = ('report', 'expert', 'ratings', 'remark', 'submit_date')
	choise_display = 'expert'
admin.site.register(PatentPackage, PatentPackageAdmin)
admin.site.register(PatentRatingReport, PatentRatingReportAdmin)
admin.site.register(PatentExpertRating, PatentExpertRatingAdmin)
