# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import *
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.core import exceptions
import json

class PatentRatingDetailView(SuccessMessageMixin, UpdateView):
	error_message = u'"%(name)s" 评价失败'
	default_referer_url = '/'

	def get_context_data(self, **kwargs):
		context = super(PatentRatingDetailView, self).get_context_data(**kwargs)
		context['request'] = self.request
		context['patent'] = self.object.patent.patent
		context['history_rating'] = self.model.objects.filter(patent__patent=self.object.patent.patent).exclude(patent=self.object.patent).exclude(submit_date=None).exclude(rank=-1).order_by("submit_date")
		if '__next__' in self.request.POST:
			context['i__next__'] = self.request.POST['__next__']
		else:
			if 'HTTP_REFERER' in self.request.META:
				context['i__next__'] = self.request.META['HTTP_REFERER']
			else:
				context['i__next__'] = reverse_lazy('patent-rating-list')

		return context

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(cleaned_data, **{'name':self.object.patent.patent.name})

	def get_success_url(self):
		return self.request.POST['__next__']

	def form_invalid(self, form):
		error_msg = u'信息更新失败'
		messages.error(self.request, error_msg)
		return super(PatentRatingDetailView, self).form_invalid(form)
