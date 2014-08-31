# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.http import Http404
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from django.core import exceptions
from django.core.files.base import File
from django.db.models import Q
from libs.django_datatables_view.base_datatable_view import BaseDatatableView
from filetransfers.api import serve_file
import os

from retrvhome.models import *
from retrvhome.forms import *


class RetrvHomeView(TemplateView):
    year_list = [year for year in range(2000, 2013)]
    type_list = ['发明专利', '实用新型', '外观设计']

    def get_context_data(self, **kwargs):
        context = super(RetrvHomeView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['year_list'] = self.year_list
        context['type_list'] = self.type_list
        context['patent_year_count'] = self.get_patent_count_by_year(self.year_list, self.type_list)
        return context

    def get_patent_count_by_year(self, year_list, type_list):
        year_count = {}
        for year in year_list:
            patent_count = []
            for type in type_list:
                q_apply = Patent.objects.filter(type=type, apply_date__startswith=year)
                q_authorize = Patent.objects.filter(type=type, authorize_date__startswith=year)
                patent_count.append([q_apply.count(), q_authorize.count()])
            year_count[year] = patent_count
        return year_count


class RetrvListView(ListView, FormMixin):
    field_display_width = {}
    retrieve_list = 'retrieve_list'

    def get_context_data(self, **kwargs):
        context = super(RetrvListView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['form'] = self.form
        context[self.retrieve_list] = self.model.objects.filter(retrieve=True).order_by('sort')
        return context

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        return super(RetrvListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        object_list = self.model.objects.filter(display=True).order_by('sort')
        if not object_list:
            raise Http404
        for o in object_list:
            o.width = self.field_display_width.get(o.field_name, None)
        return object_list


class RetrvListJson(BaseDatatableView):
    columns = []
    model = None
    field_model = None
    column_template = {}

    def __init__(self, *args, **kwargs):
        super(RetrvListJson, self).__init__(*args, **kwargs)
        if not self.columns:
            self.columns = ['pk', 'DT_RowId']
            field_list = self.field_model.objects.filter(display=True).order_by('sort')
            if not field_list:
                raise Http404
            for field in field_list:
                self.columns.append(field.field_name)

    def filter_queryset(self, qs):
        q = Q()
        retrieve_list = self.field_model.objects.filter(retrieve=True)
        for field in retrieve_list:
            if field.field_name in self.request.GET:
                q &= Q(("%s__icontains" % field.field_name, self.request.GET.get(field.field_name)))
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            q &= Q(name__icontains=sSearch)
        return qs.filter(q)

    def render_column(self, row, column):
        if column in self.column_template:
            return self.column_template[column](row)
        if column == 'DT_RowId':
            return '%d' % (row.pk)
        elif column == 'authorize_code':
            if row.authorize_code:
                return u'<a href="#">%s</a>' % row.authorize_code
            else:
                return row.state
        return super(RetrvListJson, self).render_column(row, column)


class FileServeView(View):
    base_dir = ''
    ext_list = ["pdf", "jpg", "jpeg", "png"]

    def get(self, request, *args, **kwargs):
        fcode = kwargs["fcode"]
        file = None
        for ext in self.ext_list:
            filename = self.base_dir + fcode + "." + ext
            if os.path.exists(filename):
                file = File(None, filename)
                file.open('r')
                break
        if not file:
            raise Http404
        return serve_file(request, file, save_as=False)

    def exist(self, type, fcode):
        base_dir = {'rankfile': 'files/patent/rank/', 'specfile': 'files/patent/spec/'}[type]
        for ext in self.ext_list:
            filename = base_dir + fcode + "." + ext
            print filename
            if os.path.exists(filename):
                return True
        return False

