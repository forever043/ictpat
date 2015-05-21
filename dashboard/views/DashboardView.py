# -*- coding: UTF-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from libs.chartit import DataPool, Chart

from patmgr.models import Patent, Department

# Create your views here.
class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['request'] = self.request

        qs_pat = Department.objects.annotate(patent_count=Count('patent'))
        qs_scr = Department.objects.annotate(scr_count=Count('softwarecr'))

        ds = DataPool(
            series=
            [{'options': {
                'source': qs_pat},
              'terms': [{'p_name': 'name'}, 'patent_count']},
             {'options': {
                 'source': qs_scr},
              'terms': [{'s_name': 'name'}, 'scr_count']}
            ])
        cht = Chart(
            datasource=ds,
            series_options=[
                {
                    'options': {
                        'type': 'column',
                        'yAxis': 0,
                        'stacking': False},
                    'terms': {
                        'p_name': ['patent_count'],
                    }
                },
                {
                    'options': {
                        'type': 'column',
                        'yAxis': 1,
                        'stacking': False},
                    'terms': {
                        's_name': ['scr_count'],
                    }
                }
            ],
            chart_options={
                'title': {'text': '部门知识产权统计'},
                'chart': {'height': '450'},
                'xAxis': {
                    'title': {'text': '部门'}
                },
                'yAxis': [
                    {'title': {'text': '专利数'}},
                    {'title': {'text': '软件登记数'}, 'opposite': True}
                ]
            }
        )

        context['patentchart'] = cht
        return context

    def get(self, request, *args, **kwargs):
        if request.user.has_perm('dashboard.operator'):
            return super(DashboardView, self).get(request, args, kwargs)
        elif request.user.has_perm('dashboard.expert'):
            return HttpResponseRedirect(reverse_lazy('patent-rating-list'))
        else:
            return HttpResponseRedirect('/dashboard/login/')
