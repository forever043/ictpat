from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required

from scrmgr.models import *
from scrmgr.forms import *
from dashboard.views import *

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
)

