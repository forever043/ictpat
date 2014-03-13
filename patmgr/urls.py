# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required

from patmgr.views import PatentRetrvSchemeView, RetrvSchemeExport, PatentListJson, PatentBatchAddView
from dashboard.views import *
from patmgr.forms import *


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
    url(r'^list/data/$', 	login_required(PatentListJson.as_view()), name='patent-list-json'),

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
				form_class = PatentRankForm,
				template_name = 'patmgr/patent_rank.html',
				success_message = u'专利 "%(name)s" 评价成功',
				error_message = u'专利 "%(name)s" 评价失败')),
		name='patent-rank'),


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
    url(r'^retrvmgr/$',			login_required(PatentRetrvSchemeView.as_view()), name='patent-retrvscheme'),
	url(r'^retrvmgr/export/$',	login_required(RetrvSchemeExport.as_view()), name='patent-retrvscheme-export'),

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
				}
		)),
		name='patent-import'),

	# Patent File
	url(r'^file/$',			TemplateView.as_view(template_name='patmgr/patent_file_upload.html'), name='patent-file'),
	#url(r'^file/upload/$',	PatentFileUploadView.as_view(), name='patent-file-upload'),
	url(r'^file/upload/$',
		FileUploadView.as_view(
			model = Patent,
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

