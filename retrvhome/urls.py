from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView

urlpatterns = patterns('',
	url(r'^$',	TemplateView.as_view(template_name='retrvhome/index.html'), name='retrvhome-index'),
)

