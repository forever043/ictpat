# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from django.core import exceptions

from retrvhome.models import *
from retrvhome.forms import *

class RetrvListView(ListView, FormMixin):
	paginate_by = 10

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
		query_filter_list = self.request.session.get('query-filter', {})
		messages.warning(self.request, query_filter_list)
		object_filter = {}
		for (filter_name, filter_value) in query_filter_list.items():
                        if 'pk' in filter_value:
                                object_filter[filter_name] = filter_value['pk']
                        elif 'str' in filter_value:
                                object_filter[filter_name + '__icontains'] = filter_value['str']
		object_list = self.model.objects.filter(**object_filter)
		if not object_list:
			messages.warning(self.request, "没有找到符合条件的专利")

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


