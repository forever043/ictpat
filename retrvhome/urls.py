from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from retrvhome.models import Patent, PatentField
from retrvhome.forms import RetrvFilterForm
from retrvhome.views import *

urlpatterns = patterns('',
	url(r'^$',			TemplateView.as_view(template_name='retrvhome/index.html'), name='retrvhome-index'),

	# Patent
	url(r'^patent/$',
		RetrvListView.as_view(
				model = PatentField,
				form_class = RetrvFilterForm,
				context_object_name = 'field_list',
				retrieve_list = 'retrieve_list',
				template_name = 'retrvhome/patent_list.html',
				field_display_width = {
					"name": 25,
					"department": 13,
					"inventors": 20,
					"type": 8,
					"apply_code": 10,
					"apply_date": 8,
					"authorize_code": 10,
				},
				success_url = reverse_lazy('patent-list')),
		name='retrvhome-patent-list'),
    url(r'^patent/data/$', 
		PatentListJson.as_view(
			model = Patent,
			field_model = PatentField,
			column_template = {
				"name":				lambda o: u'<a href="#">%s</a>' % o.name,
				"apply_code":		lambda o: u'<a href="%(url)s" target="_blank">%(name)s</a>' % {
													"url":	reverse_lazy('patent-file-service', args=[o.apply_code]),
													"name":	o.apply_code},
				"authorize_code":	lambda o: u'<a href="%(url)s" target="_blank">%(name)s</a>' % {
													"url":	reverse_lazy('patent-file-service', args=[o.authorize_code]),
													"name":	o.authorize_code }
												if o.authorize_code  else o.state,
			}),
		name='retrvhome-patent-list-json'),

	# SoftwareCR
	url(r'^scr/$',		TemplateView.as_view(template_name='retrvhome/index.html'), name='retrvhome-scr-list'),
)

