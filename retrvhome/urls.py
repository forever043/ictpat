from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required

from retrvhome.models import Patent, PatentField
from retrvhome.forms import RetrvFilterForm
from retrvhome.views import *

urlpatterns = patterns('',
    url(r'^$', RetrvHomeView.as_view(template_name='retrvhome/index.html'), name='retrvhome-index'),

    # Patent
    url(r'^patent/$',
        RetrvListView.as_view(
                model = PatentField,
                form_class = PatentRetrvFilterForm,
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
        RetrvListJson.as_view(
            model = Patent,
            field_model = PatentField,
            column_template = {
                "name":                lambda o: u'<a href="#">%s</a>' % o.name,
                "apply_code":        lambda o: u'<a href="%(url)s" target="_blank">%(name)s</a>' % {
                                                    "url":    reverse_lazy('patent-file-service', args=[o.apply_code]),
                                                    "name":    o.apply_code},
                "authorize_code":    lambda o: u'<a href="%(url)s" target="_blank">%(name)s</a>' % {
                                                    "url":    reverse_lazy('patent-file-service', args=[o.authorize_code]),
                                                    "name":    o.authorize_code }
                                                if o.authorize_code  else o.state,
            }),
        name='retrvhome-patent-list-json'),

    # SoftwareCR
    url(r'^scr/$',
        RetrvListView.as_view(
                model = RetrvSoftwareCRField,
                form_class = SoftwareCRRetrvFilterForm,
                context_object_name = 'field_list',
                retrieve_list = 'retrieve_list',
                template_name = 'retrvhome/scr_list.html',
                field_display_width = {
                    "name": 25,
                    "department": 13,
                    "developers": 20,
                    "authorize_code": 10,
                },
                success_url = reverse_lazy('scr-list')),
        name='retrvhome-scr-list'),
    url(r'^scr/data/$', 
        RetrvListJson.as_view(
            model = RetrvSoftwareCR,
            field_model = RetrvSoftwareCRField,
            column_template = {
                "name":              lambda o: u'<a href="#">%s</a>' % o.name,
                "authorize_code":    lambda o: u'<a href="%(url)s" target="_blank">%(name)s</a>' % {
                                                    "url":    reverse_lazy('scr-file-service', args=[o.authorize_code]),
                                                    "name":    o.authorize_code }
                                                if o.authorize_code  else o.state,
            }),
        name='retrvhome-scr-list-json'),

    # FileServ
    url(r'^file/(?P<fcode>.+)/apply/$',
        FileServeView.as_view(base_dir='files/patent/apply/'),
        name='patent-apply-file-service'),
    url(r'^file/(?P<fcode>.+)/auth/$',
        FileServeView.as_view(base_dir='files/patent/auth/'),
        name='patent-auth-file-service'),
    url(r'^file/(?P<fcode>.+)/rank/(?P<fname>.+).pdf$',
        login_required(FileServeView.as_view(base_dir='files/patent/rank/',
            ext_list = ["pdf"])),
        name='patent-rank-file-service'),
    url(r'^file/(?P<fcode>.+)/spec/(?P<fname>.+).pdf$',
        login_required(FileServeView.as_view(base_dir='files/patent/spec/',
            ext_list = ["pdf"])),
        name='patent-spec-file-service'),
)

