# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required

from scrmgr.models import *
from scrmgr.forms import *
import scrmgr.forms
from dashboard.views import *

import scrmgr.models
import retrvhome.models

urlpatterns = patterns('scrmgr.views',
    url(r'^$', 'scrmgr'),

	# SoftwareCR List
    url(r'^list/fresh/$',
		login_required(DashMgrFreshListView.as_view(
				pattern_name='scr-list')),
		name='scr-list-fresh'),
    url(r'^list/$',
		login_required(DashMgrListView.as_view(
				model = SoftwareCR,
				form_class = SoftwareCRFilterForm,
				context_object_name = 'scr_list',
				template_name = 'scrmgr/scr_list.html',
				success_url = reverse_lazy('scr-list'))),
		name='scr-list'),

	# SoftwareCR Details
    url(r'^(?P<pk>\d+)/$',
		login_required(DashMgrDetailView.as_view(
				model = SoftwareCR,
				context_object_name = 'scr',
				template_name='scrmgr/scr_detail.html',
				default_referer_url = reverse_lazy('scr-list'))),
		name='scr-detail'),
    url(r'^add/$',
		login_required(DashMgrCreateView.as_view(
				model = SoftwareCR,
				form_class = SoftwareCRExtForm,
				template_name = 'scrmgr/add_scr_basic.html',
				success_url = reverse_lazy('scr-add'),
				success_message = u'软件 "%(name)s" 添加成功',
				error_message = u'软件添加失败')),
		name='scr-add'),
	url(r'^(?P<pk>\d+)/edit/$',
		login_required(DashMgrUpdateView.as_view(
				model = SoftwareCR,
				extfield_model = SoftwareCRExtField,
				extfield_ref = 'scr',
				form_class = SoftwareCRExtForm,
				template_name = 'scrmgr/scr_edit.html',
				success_message = u'软件 "%(name)s" 信息更新成功',
				error_message = u'软件 "%(name)s" 信息更新失败')),
		name='scr-edit'),
	url(r'^(?P<pk>\d+)/delete/$',
		login_required(DashMgrDeleteView.as_view(
				model = SoftwareCR,
				success_url = reverse_lazy('scr-list'))),
		name='scr-delete'),
	url(r'^(?P<pk>\d+)/rank/$',
		login_required(DashMgrRankView.as_view(
				model = SoftwareCRRank,
				ref_model = SoftwareCR,
				ref_name = 'scr',
				form_class = SoftwareCRRankForm,
				template_name = 'scrmgr/scr_rank.html',
				default_referer_url = reverse_lazy('scr-list'),
				success_message = u'软件 "%(name)s" 评价成功',
				error_message = u'软件 "%(name)s" 评价失败')),
		name='scr-rank'),

	# Patent MetaField Manager
	url(r'^meta/$',
		login_required(TemplateView.as_view(template_name='scrmgr/scr_extfield.html')),
		name='scr-extfield'),
	url(r'^meta/extfield/data/$',
		login_required(ExtFieldJson.as_view(model=SoftwareCRExtFieldType)),
		name='scr-extfield-json'),

	# Patent Retrieve Manager
    url(r'^retrvmgr/$',
		login_required(RetrvSchemeView.as_view(
			template_name = 'scrmgr/scr_retrvmgr.html',
			scheme_model = scrmgr.models.RetrvScheme,
			builtinfield_model = scrmgr.models.BuiltinRetrvField,
			customizedfield_model = scrmgr.models.CustomizedRetrvField,
			form_class = SoftwareCRRetrvSchemeForm,
			success_url = reverse_lazy('scr-retrvscheme'))),
		name='scr-retrvscheme'),
	url(r'^retrvmgr/export/$',
		login_required(RetrvSchemeExport.as_view(
			model = SoftwareCR,
			extfield_model = SoftwareCRExtField,
			ref_name = 'scr',
			builtin_field_model		= scrmgr.models.BuiltinRetrvField,
			customized_field_model	= scrmgr.models.CustomizedRetrvField,
			retrv_model				= retrvhome.models.RetrvSoftwareCR,
			retrv_field_model		= retrvhome.models.RetrvSoftwareCRField,
			return_url = reverse_lazy('scr-retrvscheme'))),
		name='scr-retrvscheme-export'),

	# SoftwareCR ImportWizard View
    url(r'^import/',
		login_required(ImportWizardView.as_view(
				model=SoftwareCR,
				form_list = [
    				#("import_config", PatentImportForm),
    				("db_select",     scrmgr.forms.UploadXlsxFileForm),
    				("matchfield",    scrmgr.forms.MatchFieldForm),
				],
				template_list = {
    				"import_config": "scrmgr/import/import_config.html",
    				"db_select":     "scrmgr/import/db_select.html",
    				"matchfield":    "scrmgr/import/matchfield.html",
				},
				return_url = reverse_lazy('scr-import'),
		)),
		name='scr-import'),


	# SoftwareCR File
	url(r'^file/$', TemplateView.as_view(template_name='scrmgr/scr_file_upload.html'), name='scr-file'),
	url(r'^file/upload/$',
		FileUploadView.as_view(
			model = SoftwareCR,
			file_service_view = "scr-file-service",
			fcode_map = {
				"authorize_code": "authorize_file"
			}),
		name='scr-file-upload'),
	url(r'^file/(?P<fcode>.+)/$',
		FileServeView.as_view(
			model = SoftwareCR,
			fcode_map = {
				"authorize_code": "authorize_file"
			}),
		name='scr-file-service'),
)

