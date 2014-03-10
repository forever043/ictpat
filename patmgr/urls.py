from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required

from patmgr.views import *

urlpatterns = patterns('',
    url(r'^$',			  RedirectView.as_view(pattern_name='patent-list'), name='patent'),

	# Patent List
    url(r'^list/$',			login_required(PatentListView.as_view()),	name='patent-list'),
    url(r'^list/fresh/$',	login_required(PatentFreshListView.as_view(pattern_name='patent-list')), name='patent-list-fresh'),
    url(r'^list/data/$', 	login_required(PatentListJson.as_view()), name='patent-list-json'),

	# Patent Details
    url(r'^add/$',		  PatentCreateView.as_view(),	name='patent-add'),
    url(r'^add/batch/$',	  PatentBatchAddView.as_view(),	name='patent-batchadd'),
    url(r'^(?P<pk>\d+)/$',	  PatentDetailView.as_view(),	name='patent-detail'),
    url(r'^(?P<pk>\d+)/edit/$',	  PatentUpdateView.as_view(),	name='patent-edit'),
    url(r'^(?P<pk>\d+)/delete/$', PatentDeleteView.as_view(),	name='patent-delete'),
	url(r'^(?P<pk>\d+)/rank/$', PatentRankView.as_view(), name='patent-rank'),

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
