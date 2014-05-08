# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required

from patmgr.views import PatentBatchAddView
from dashboard.views import *
from patmgr.forms import *

import patmgr.models
import retrvhome.models


urlpatterns = patterns('',
    url(r'^$', login_required(RedirectView.as_view(pattern_name='patent-list')), name='patent'),

	# Patent List
    url(r'^list/fresh/$',
		login_required(DashMgrFreshListView.as_view(
				pattern_name='patent-list')),
		name='patent-list-fresh'),
    url(r'^list/$',
		login_required(DashMgrListView.as_view(
				model = Patent,
				form_class = PatentFilterForm,
				context_object_name = 'patent_list',
				template_name = 'patmgr/list_patent.html',
				success_url = reverse_lazy('patent-list'))),
		name='patent-list'),
    #url(r'^list/data/$', 	login_required(PatentListJson.as_view()), name='patent-list-json'),
    url(r'^list/data/$', 
        login_required(DashMgrListJson.as_view(
            model = Patent,
            retrieve_list = [ 'department', 'state', 'type', 'name', 'inventors', 'apply_code', 'authorize_code' ],
            columns = [ 'department', 'name', 'inventors', 'apply_code', 'apply_date', 'authorize_code' ],
            column_template = { 
                "name":             lambda o: u'<a href="%(url)s">%(name)s</a>' % {
                                                    "url":  reverse_lazy('patent-detail', args=[o.pk]),
                                                    "name": o.name},
                "department":		lambda o: u'%s' % o.department.name,
                "apply_code":       lambda o: u'<a href="%(url)s" target="_blank">%(name)s</a>' % { 
                                                    "url":  reverse_lazy('patent-file-service', args=[o.apply_code]),
                                                    "name": o.apply_code},
                "authorize_code":   lambda o: u'<a href="%(url)s" target="_blank">%(name)s</a>' % { 
                                                    "url":  reverse_lazy('patent-file-service', args=[o.authorize_code]),
                                                    "name": o.authorize_code }
                                                if o.authorize_code  else o.state.name,
           
                "pk":               lambda o: u'<a href="%(edit_url)s" title="修改"><img src="/resources/images/icons/pencil.png" alt="Edit" />修改</a>' \
						                      u'<!--<a href="#" class="delete" title="删除"><img src="/resources/images/icons/cross.png" alt="Delete" /></a>-->' \
						                      u'&nbsp;&nbsp;<a href="%(rank_url)s" title="评级">' \
                                                    u'<img src="/resources/images/icons/hammer_screwdriver.png" alt="Edit Meta" />评级</a>'
                                              % {
                                                    "edit_url":  reverse_lazy('patent-edit', args=[o.pk]),
                                                    "rank_url":  reverse_lazy('patent-rank', args=[o.pk]),
                                              }
            })), 
        name='patent-list-json'),

	# Patent Details
    url(r'^(?P<pk>\d+)/$',
		login_required(DashMgrDetailView.as_view(
				model = Patent,
				context_object_name = 'patent',
				template_name='patmgr/patent_detail.html',
				default_referer_url = reverse_lazy('patent-list'))),
		name='patent-detail'),
    url(r'^add/$',
		login_required(DashMgrCreateView.as_view(
				model = Patent,
				form_class = PatentExtForm,
				template_name = 'patmgr/add_patent_basic.html',
				success_url = reverse_lazy('patent-add'),
				success_message = u'专利 "%(name)s" 添加成功',
				error_message = u'专利添加失败')),
		name='patent-add'),
    url(r'^add/batch/$',	  PatentBatchAddView.as_view(),	name='patent-batchadd'),
	url(r'^(?P<pk>\d+)/edit/$',
		login_required(DashMgrUpdateView.as_view(
				model = Patent,
				extfield_model = PatentExtField,
				extfield_ref = 'patent',
				form_class = PatentExtForm,
				template_name = 'patmgr/edit_patent.html',
				success_message = u'专利 "%(name)s" 信息更新成功',
				error_message = u'专利 "%(name)s" 信息更新失败')),
		name='patent-edit'),
	url(r'^(?P<pk>\d+)/delete/$',
		login_required(DashMgrDeleteView.as_view(
				model = Patent,
				success_url = reverse_lazy('patent-list'))),
		name='patent-delete'),
	url(r'^(?P<pk>\d+)/rank/$',
		login_required(DashMgrRankView.as_view(
				model = PatentRank,
				ref_model = Patent,
				ref_name = 'patent',
				form_class = PatentRankForm,
				template_name = 'patmgr/patent_rank.html',
				default_referer_url = reverse_lazy('patent-list'),
				success_message = u'专利 "%(name)s" 评价成功',
				error_message = u'专利 "%(name)s" 评价失败')),
		name='patent-rank'),

	# Patent Rating Manager
	url(r'^package/$',
		login_required(TemplateView.as_view(template_name='patmgr/patent_package_list.html')),
		name='patent-package-list'),
    url(r'^package/list/data/$', 
        login_required(DashMgrListJson.as_view(
            model = PatentPackage,
            retrieve_list = [],
            columns = [ 'name', 'state', 'submit_date', 'finish_date' ],
            column_template = { 
                "name":             lambda o: u'<a href="%(url)s">%(name)s</a>' % {
                                                    "url":  reverse_lazy('patent-package-detail', args=[o.pk]),
                                                    "name": o.name},
                "state":			lambda o: u'%s' % u'已完成' if o.finish_date else u'进行中',
                "pk":               lambda o: u'<a href="%(detail_url)s" title="查看"><img src="/resources/images/icons/pencil.png" alt="查看" />查看</a>&nbsp;&nbsp;' \
						                      u'<a href="%(export_url)s" title="导出"><img src="/resources/images/icons/hammer_screwdriver.png" alt="导出" />导出</a>'
                                              % {
                                                    "detail_url":  reverse_lazy('patent-package-detail', args=[o.pk]),
                                                    "export_url":  reverse_lazy('patent-package-detail', args=[o.pk]),
                                              }
            })), 
        name='patent-package-list-json'),
    url(r'^package/(?P<pk>\d+)/$',
		login_required(DashMgrDetailView.as_view(
				model = PatentPackage,
				context_object_name = 'patpkg',
				template_name='patmgr/patent_package_detail.html',
				default_referer_url = reverse_lazy('patent-package-list'))),
		name='patent-package-detail'),
    url(r'^package/(?P<pk>\d+)/data/$',
        login_required(DashMgrListJson.as_view(
            model = PatentExpertRating,
            retrieve_list = ["package"],
            columns = [ 'patent', 'expert', 'rank', 'remark', 'state', 'submit_date' ],
            column_template = { 
				"patent":			lambda o: u'%s<span style="float:right;"><a href="#">撰写评级报告</a></span>' % o.patent.patent.name,
                "expert":           lambda o: u'%s' % o.expert.last_name + o.expert.first_name,
                "state":			lambda o: u'%s' % u'已完成' if o.submit_date else u'进行中',
                "pk":               lambda o: u'<a href="%(url)s" title="更换专家"><img src="/resources/images/icons/hammer_screwdriver.png" alt="更换专家" />更换专家</a>'
                                              % { "url":  reverse_lazy('patent-package-detail', args=[o.pk]) } if not o.submit_date else u''
            })), 
        name='patent-package-detail-json'),

	# Patent MetaField Manager
	url(r'^meta/$',
		login_required(TemplateView.as_view(template_name='patmgr/extfield.html')),
		name='patent-extfield'),
	url(r'^meta/extfield/data/$',
		login_required(ExtFieldJson.as_view(model=PatentExtFieldType)),
		name='patent-extfield-json'),
	url(r'^meta/patenttype/data/$',
		login_required(MetaJson.as_view(model=PatentType)),
		name='patent-type-json'),
	url(r'^meta/patentstate/data/$',
		login_required(MetaJson.as_view(model=PatentState)),
		name='patent-state-json'),

	# Patent Retrieve Manager
    url(r'^retrvmgr/$',
		login_required(RetrvSchemeView.as_view(
			template_name = 'patmgr/retrvmgr.html',
			scheme_model = RetrvScheme,
			builtinfield_model = BuiltinRetrvField,
			customizedfield_model = CustomizedRetrvField,
			form_class = PatentRetrvSchemeForm,
			success_url = reverse_lazy('patent-retrvscheme'))),
		name='patent-retrvscheme'),
	#url(r'^retrvmgr/export/$',	login_required(RetrvSchemeExport.as_view()), name='patent-retrvscheme-export'),
	url(r'^retrvmgr/export/$',
		login_required(RetrvSchemeExport.as_view(
			model = Patent,
			extfield_model = PatentExtField,
			ref_name = 'patent',
			builtin_field_model		= patmgr.models.BuiltinRetrvField,
			customized_field_model	= patmgr.models.CustomizedRetrvField,
			retrv_model				= retrvhome.models.Patent,
			retrv_field_model		= retrvhome.models.PatentField,
			return_url = reverse_lazy('patent-retrvscheme'))),
		name='patent-retrvscheme-export'),

	# Patent ImportWizard View
    url(r'^import/',
		login_required(ImportWizardView.as_view(
				model=Patent,
				form_list = [
    				#("import_config", PatentImportForm),
    				("db_select",     UploadXlsxFileForm),
    				("matchfield",    MatchFieldForm),
				],
				template_list = {
    				"import_config": "patmgr/import/import_config.html",
    				"db_select":     "patmgr/import/db_select.html",
    				"matchfield":    "patmgr/import/matchfield.html",
				},
				return_url = reverse_lazy('patent-import'),
		)),
		name='patent-import'),

	# Patent File
	url(r'^file/$',			TemplateView.as_view(template_name='patmgr/patent_file_upload.html'), name='patent-file'),
	url(r'^file/upload/$',
		FileUploadView.as_view(
			model = Patent,
			file_service_view = "patent-file-service",
			fcode_map = {
				"apply_code": "apply_file",
				"authorize_code": "authorize_file"
			}),
		name='patent-file-upload'),
	url(r'^file/(?P<fcode>.+)/$',
		FileServeView.as_view(
			model = Patent,
			fcode_map = {
				"apply_code": "apply_file",
				"authorize_code": "authorize_file"
			}),
		name='patent-file-service'),
)

