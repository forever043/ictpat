from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from retrvhome.models import Patent, PatentField
from retrvhome.forms import RetrvFilterForm
from retrvhome.views import *

urlpatterns = patterns('',
	url(r'^$',			TemplateView.as_view(template_name='retrvhome/index.html'), name='retrvhome-index'),
	url(r'^patent/$',
		RetrvListView.as_view(
				model = PatentField,
				form_class = RetrvFilterForm,
				context_object_name = 'field_list',
				template_name = 'retrvhome/patent_list.html',
				success_url = reverse_lazy('patent-list')),
		name='retrvhome-patent-list'),
    url(r'^patent/data/$', 	PatentListJson.as_view(), name='retrvhome-patent-list-json'),
	url(r'^scr/$',		TemplateView.as_view(template_name='retrvhome/index.html'), name='retrvhome-scr-list'),
)

