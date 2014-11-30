# -*- coding: UTF-8 -*-
from django.contrib import admin
from rankmgr.models import *

# 专利评价管理
class PatentPackageAdmin(admin.ModelAdmin):
	list_display = ('name', 'desc', 'rating_weight', 'submit_date', 'finish_date')
	choise_display = 'name'
class PatentPackageCatalogWeightAdmin(admin.ModelAdmin):
    list_display = ('package', 'catalog', 'weight')
    choise_display = 'package'
class PatentPackageRankItemAdmin(admin.ModelAdmin):
	list_display = ('package', 'item', 'weight')
	choise_display = 'item'
class PatentRatingReportAdmin(admin.ModelAdmin):
	list_display = ('package', 'patent', 'rating', 'rank', 'report', 'finish_date')
	choise_display = 'patent'
class PatentExpertRatingAdmin(admin.ModelAdmin):
	list_display = ('report', 'expert', 'ratings', 'remark', 'submit_date')
	choise_display = 'expert'
class RatingSelectAdmin(admin.ModelAdmin):
	list_display = ('rating', 'item', 'select')
	choise_display = 'rating'
admin.site.register(PatentPackage, PatentPackageAdmin)
admin.site.register(PatentPackageCatalogWeight, PatentPackageCatalogWeightAdmin)
admin.site.register(PatentPackageRankItem, PatentPackageRankItemAdmin)
admin.site.register(PatentRatingReport, PatentRatingReportAdmin)
admin.site.register(PatentExpertRating, PatentExpertRatingAdmin)
admin.site.register(RatingSelect, RatingSelectAdmin)


class ExpertCatalogWeightAdmin(admin.ModelAdmin):
    list_display = ('package', 'expert_catalog', 'rank_catalog', 'weight')
    choise_display = 'expert_catalog'
admin.site.register(ExpertCatalogWeight, ExpertCatalogWeightAdmin)

# 评分项目库
class RankCatalogAdmin(admin.ModelAdmin):
	list_display = ('name', 'sort', 'disabled', 'desc')
	choise_display = 'name'
class RankOptionAdmin(admin.ModelAdmin):
	list_display = ('name', 'index')
	choise_display = 'name'
class RankItemAdmin(admin.ModelAdmin):
	list_display = ('catalog', 'desc', 'optNr', 'optA', 'optB', 'optC', 'optD', 'optE', 'optF')
	choise_display = 'desc'
admin.site.register(RankCatalog, RankCatalogAdmin)
admin.site.register(RankOption, RankOptionAdmin)
admin.site.register(RankItem, RankItemAdmin)

