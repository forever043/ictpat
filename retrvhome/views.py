# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.http import Http404
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from django.core import exceptions
from django.db.models import Q
from libs.django_datatables_view.base_datatable_view import BaseDatatableView

from retrvhome.models import *
from retrvhome.forms import *

class RetrvListView(ListView, FormMixin):
	field_display_width = {
		"name": 25,
		"department": 13,
		"inventors": 20,
		"type": 8,
		"apply_code": 10,
		"apply_date": 8,
		"authorize_code": 10,
	}

	def get_context_data(self, **kwargs):
		context = super(RetrvListView, self).get_context_data(**kwargs)
		context['request'] = self.request
		context['form'] = self.form
		return context

	def get(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		self.form = self.get_form(form_class)
		return super(RetrvListView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid():
			self.form_valid(form)
		else:
			self.form_invalid(form)  
		return self.get(request, *args, **kwargs)

	def get_initial(self):
		initial = {}
		query_filter_list = self.request.session.get('query-filter', {})
		for (filter_name, filter_value) in query_filter_list.items():
			if 'pk' in filter_value:
				initial[filter_name] = filter_value['pk']
			elif 'str' in filter_value:
				initial[filter_name] = filter_value['str']
		return initial

	def get_queryset(self):
		object_list = self.model.objects.filter(display=True).order_by('sort')
		if not object_list:
			raise Http404
		for o in object_list:
			o.width = self.field_display_width.get(o.field_name, None)
		return object_list

	def form_valid(self, form):
		filter = {}
		for (field, value) in form.cleaned_data.items():
			if value:
				if isinstance(value, models.Model):
					filter[field] = {'pk': value.pk}
				else:
					#filter[field+'__icontains'] = value
					filter[field] = {'str': value}
		self.request.session['query-filter'] = filter
		return super(RetrvListView, self).form_valid(form)

	def form_invalid(self, form):
		return super(RetrvListView, self).form_invalid(form)


class PatentListJson(BaseDatatableView):
	model = Patent
	field_model = PatentField
	columns = []
	#columns = ['department', 'name', 'inventors', 'apply_code', 'apply_date', 'authorize_code', 'pk', 'DT_RowId']
	#order_columns = ['field_label', 'field_name', '', '', 'sort', 'pk', 'pk']
	#max_display_length = 2000

	def __init__(self, *args, **kwargs):
		super(PatentListJson, self).__init__(*args, **kwargs)
		if not self.columns:
			self.columns = [ 'pk', 'DT_RowId' ]
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
				q &= Q(("%s__icontains"%field.field_name, self.request.GET.get(field.field_name)))
		sSearch = self.request.GET.get('sSearch', None)
		if sSearch:
			q &= Q(name__icontains=sSearch)
		return qs.filter(q)

	def render_column(self, row, column):
		if column == 'DT_RowId':
			return '%d' % (row.pk)
		elif column == 'name':
			return u'<a href="#">%s</a>' % row.name
		elif column == 'apply_code':
			return u'<a href="#">%s</a>' % row.apply_code
		elif column == 'authorize_code':
			if row.authorize_code:
				return u'<a href="#">%s</a>' % row.authorize_code
			else:
				return row.state
		return super(PatentListJson, self).render_column(row, column)

