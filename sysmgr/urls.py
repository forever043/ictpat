from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView, CreateView, UpdateView

from sysmgr.views import *
from dashboard.forms import ExpertProfileForm

urlpatterns = patterns('',
    url(r'^$',         RedirectView.as_view(pattern_name='sysmgr-meta'), name='sysmgr'),
    url(r'^meta/$',    MetaMgrView.as_view(),							name='sysmgr-meta'),
    url(r'^import/$',  TemplateView.as_view(template_name='sysmgr/import.html'), name='sysmgr-import'),
    url(r'^upload/$',  TemplateView.as_view(template_name='sysmgr/file_upload.html'), name='sysmgr-upload'),
    url(r'^profile/$', UpdateView.as_view(template_name='sysmgr/profile.html', model=User, form_class=ExpertProfileForm), name='sysmgr-profile'),
)

