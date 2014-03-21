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
		qs2 = Department.objects.annotate(scr_count=Count('softwarecr'))

		ds = DataPool(
			series =
				[{'options': {
					'source': qs},
				  'terms': ['name', 'patent_count']},
				 {'options': {
					'source': qs2},
				  'terms': [
					{'s_name': 'name'}, 'scr_count']}
				])
		cht = Chart(
			datasource = ds,
			series_options = 
				[{'options': {
					'type': 'column',
					'yAxis': 0,
					'stacking': False},
				  'terms': {
					'name': ['patent_count'],
				}},
				{'options': {
					'type': 'column',
					'yAxis': 1,
					'stacking': False},
				  'terms': {
					's_name': ['scr_count'],
				}}
				],
			chart_options = 
				{ 'title': {
					'text': '部门知识产权统计'},
			  	  'xAxis': {
					'title': { 'text': '部门'}},
				  'yAxis': [
					{ 'title': { 'text': '专利数' } },
					{ 'title': { 'text': '软件登记数'}, 'opposite': True }]
				})

		context['patentchart'] = cht
		return context

