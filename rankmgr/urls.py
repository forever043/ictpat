from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required

from rankmgr.views import *

urlpatterns = patterns('',
    url(r'^$', login_required(RedirectView.as_view(pattern_name='patent-list')), name='rank'),
    url(r'^summary/$', login_required(RankSummaryView.as_view()), name='rank-summary'),
    url(r'^expert/$', login_required(RankExpertListView.as_view()), name='rank-expert-list'),
)

