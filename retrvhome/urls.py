from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from retrvhome.models import Patent
from retrvhome.forms import RetrvFilterForm
from retrvhome.views import *

urlpatterns = patterns('',
	url(r'^$',			TemplateView.as_view(template_name='retrvhome/index.html'), name='retrvhome-index'),
	url(r'^patent/$',
		RetrvListView.as_view(
				model = Patent,
				form_class = RetrvFilterForm,
				context_object_name = 'patent_list',
				template_name = 'retrvhome/patent_list.html',
				success_url = reverse_lazy('patent-list')),
		name='retrvhome-patent-list'),
	url(r'^scr/$',		TemplateView.as_view(template_name='retrvhome/index.html'), name='retrvhome-scr-list'),

	url(r'^meta/$', TemplateView.as_view(template_name='retrvhome/base.html'), name='metatest'),
)

