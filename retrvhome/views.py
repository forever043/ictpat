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


class PatentListJson(BaseDatatableView):
	columns = []
	model = None
	field_model = None
	column_template = {}

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
		if column in self.column_template:
			return self.column_template[column](row)
		if column == 'DT_RowId':
			return '%d' % (row.pk)
		elif column == 'authorize_code':
			if row.authorize_code:
				return u'<a href="#">%s</a>' % row.authorize_code
			else:
				return row.state
		return super(PatentListJson, self).render_column(row, column)

