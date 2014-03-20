# -*- coding: UTF-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from django.db.models import Count
from libs.chartit import DataPool, Chart


# Create your views here.
class RankSummaryView(TemplateView):
	template_name = 'rankmgr/index.html'

	def get_context_data(self, **kwargs):
		context = super(RankSummaryView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context


class RankExpertListView(TemplateView):
	template_name = 'rankmgr/expert_list.html'

	def get_context_data(self, **kwargs):
		context = super(RankExpertListView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context
	

