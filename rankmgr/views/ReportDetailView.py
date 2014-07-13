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
import string

from rankmgr.models import PatentRatingReport, PatentExpertRating

class PatentReportDetailView(SuccessMessageMixin, UpdateView):
	model = PatentRatingReport
	error_message = u'"%(name)s" 评级报告保存失败'
	default_referer_url = '/'

	def get_context_data(self, **kwargs):
		context = super(PatentReportDetailView, self).get_context_data(**kwargs)
		context['request'] = self.request
		context['expert_rating'] = PatentExpertRating.objects.filter(report=self.object)
		self.object.rating = 0;
		self.object.rating_finished = 0;
		for o in context['expert_rating']:
			o.expert.profile = o.expert.get_profile()
			if o.ratings != "-1":
				o.ratings = o.ratings.split(',')
				o.weights = o.report.package.rating_weight.split(',')
				o.summary = 0
				for x in xrange(len(o.weights)):
					o.summary += string.atof(o.weights[x]) * string.atof(o.ratings[x])
				if o.submit_date:
					self.object.rating += o.summary
					self.object.rating_finished += 1;
		self.object.rating = self.object.rating/self.object.rating_finished;
		self.object.rank = self.object.rating/2;

		return context

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(cleaned_data, **{'name':self.object.report.name})

	def get_success_url(self):
		return self.request.POST['__next__']

	def form_invalid(self, form):
		error_msg = u'信息更新失败'
		messages.error(self.request, error_msg)
		return super(PatentReportDetailView, self).form_invalid(form)
