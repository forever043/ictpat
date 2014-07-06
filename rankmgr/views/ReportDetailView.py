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

from rankmgr.models import PatentRatingReport, PatentExpertRating

class PatentReportDetailView(SuccessMessageMixin, UpdateView):
	model = PatentRatingReport
	error_message = u'"%(name)s" 评级报告保存失败'
	default_referer_url = '/'

	def get_context_data(self, **kwargs):
		context = super(PatentReportDetailView, self).get_context_data(**kwargs)
		context['request'] = self.request
		context['expert_rating'] = PatentExpertRating.objects.filter(patent=self.object)
		return context

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(cleaned_data, **{'name':self.object.patent.name})

	def get_success_url(self):
		return self.request.POST['__next__']

	def form_invalid(self, form):
		error_msg = u'信息更新失败'
		messages.error(self.request, error_msg)
		return super(PatentReportDetailView, self).form_invalid(form)
