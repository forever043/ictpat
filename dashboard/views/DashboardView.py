# -*- coding: UTF-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from django.db.models import Count

from libs.chartit import DataPool, Chart

from patmgr.models import Patent, Department

# Create your views here.
class DashboardView(TemplateView):
	template_name = 'dashboard/index.html'

	def get_context_data(self, **kwargs):
		context = super(DashboardView, self).get_context_data(**kwargs)
		context['request'] = self.request

		qs = Department.objects.annotate(patent_count=Count('patent'))
		patentdata = DataPool(
			series =
				[{'options': {
					'source': qs},
				  'terms': ['name', 'patent_count']}
				])
		cht = Chart(
			datasource = patentdata,
			series_options = 
				[{'options': {
					'type': 'column',
					'stacking': False},
				  'terms': {
					'name': ['patent_count'],
				}}],
			chart_options = 
				{ 'title': {
					'text': '部门专利统计'},
			  	  'xAxis': {
					'title': {
						'text': '部门'}}})

		context['patentchart'] = cht
		return context

