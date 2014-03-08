# coding=utf-8
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.db.models import Count

from libs.chartit import DataPool, Chart

from patmgr.models import Patent, Department

# Create your views here.
def dashboard(request):
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

	return render_to_response("dashboard/index.html", {'patentchart':cht}, context_instance=RequestContext(request, { 'request': request}))

