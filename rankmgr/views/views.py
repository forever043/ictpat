# -*- coding: UTF-8 -*-
from django.http import Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, ListView

from django.contrib.auth.models import User

from rankmgr.models import *

# Create your views here.
class RankSummaryView(TemplateView):
    template_name = 'rankmgr/index.html'

    def get_context_data(self, **kwargs):
        context = super(RankSummaryView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context


class RankExpertListView(ListView):
    template_name = 'rankmgr/expert_list.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(RankExpertListView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self):
        expert_list = self.model.objects.filter(groups__name=u'评审专家')
        for expert in expert_list:
            expert.rating_finish = PatentExpertRating.objects.filter(expert=expert).filter(
                submit_date__gt="1900-01-01").count()
            expert.rating_total = PatentExpertRating.objects.filter(expert=expert).count()
        return expert_list

