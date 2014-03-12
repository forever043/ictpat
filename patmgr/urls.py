# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required

from patmgr.views import *
from dashboard.views import *

urlpatterns = patterns('',
    url(r'^$',			  RedirectView.as_view(pattern_name='patent-list'), name='patent'),

	# Patent List
    url(r'^list/$',			login_required(PatentListView.as_view()),	name='patent-list'),
    url(r'^list/fresh/$',	login_required(PatentFreshListView.as_view(pattern_name='patent-list')), name='patent-list-fresh'),
    url(r'^list/data/$', 	login_required(PatentListJson.as_view()), name='patent-list-json'),

	# Patent Details
    url(r'^add/batch/$',	  PatentBatchAddView.as_view(),	name='patent-batchadd'),

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
	url(r'^(?P<pk>\d+)/edit/$',
		login_required(DashMgrUpdateView.as_view(
				model = Patent,
				form_class = PatentExtForm,
				template_name = 'patmgr/edit_patent.html',
				success_message = u'专利 "%(name)s" 信息更新成功',
				error_message = u'专利 "%(name)s" 信息更新失败')),
		name='patent-edit'),
	url(r'^(?P<pk>\d+)/delete/$',
		view=login_required(DashMgrDeleteView.as_view(
				model = Patent,
				success_url = reverse_lazy('patent-list'))),
		name='patent-delete'),
	url(r'^(?P<pk>\d+)/rank/$',
		view=login_required(DashMgrRankView.as_view(
				model = PatentRank,
				form_class = PatentRankForm,
				template_name = 'patmgr/patent_rank.html',
				success_message = u'专利 "%(name)s" 评价成功',
				error_message = u'专利 "%(name)s" 评价失败')),
		name='patent-rank'),


	# Patent MetaField Manager
	url(r'^meta/$',					 login_required(TemplateView.as_view(template_name='patmgr/extfield.html')), name='patent-extfield'),
	url(r'^meta/extfield/data/$',    login_required(PatentExtFieldJson.as_view()),			    name='patent-extfield-json'),
	url(r'^meta/patenttype/data/$',  login_required(PatentMetaJson.as_view(model=PatentType)),  name='patent-type-json'),
	url(r'^meta/patentstate/data/$', login_required(PatentMetaJson.as_view(model=PatentState)), name='patent-state-json'),

    url(r'^retrvmgr/$',			login_required(PatentRetrvSchemeView.as_view()), name='patent-retrvscheme'),
	url(r'^retrvmgr/export/$',	login_required(RetrvSchemeExport.as_view()), name='patent-retrvscheme-export'),

    url(r'^import/',		  PatentImportWizard.as_view(),	name='patent-import'),

	# Patent File
	url(r'^file/$',			TemplateView.as_view(template_name='patmgr/patent_file_upload.html'), name='patent-file'),
	url(r'^file/upload/$',	PatentFileUploadView.as_view(), name='patent-file-upload'),
	url(r'^file/(?P<fcode>.+)/$', PatentFileView.as_view(), name='patent-file-service'),
)
