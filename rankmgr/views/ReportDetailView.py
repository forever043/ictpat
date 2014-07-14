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
	default_referer_url = '/'

	def get_context_data(self, **kwargs):
		context = super(PatentReportDetailView, self).get_context_data(**kwargs)
		context['request'] = self.request
		context['expert_rating'] = PatentExpertRating.objects.filter(report=self.object)

		self.object.rating = 0;
		self.object.rating_finished = 0;

		# 遍历每一个专家评分
		for o in context['expert_rating']:
			# 获取专家profile信息
			o.expert.profile = o.expert.get_profile()
			# 如果不是拒绝评价，则计算综合分
			if o.ratings != "-1":
				# 分项分值
				o.ratings = o.ratings.split(',')
				# 权重
				o.weights = o.report.package.rating_weight.split(',')
				o.summary = 0
				for x in xrange(len(o.weights)):
					o.summary += string.atof(o.weights[x]) * string.atof(o.ratings[x])
				if o.submit_date:
					self.object.rating += o.summary
					self.object.rating_finished += 1

		# 评级为计算汇总得出；如果没有保存的评级，根据专家评分给出默认值；
		self.object.rating = self.object.rating/self.object.rating_finished if self.object.rating_finished else 0
		if not self.object.rank:
			self.object.rank = self.object.rating/2

		return context

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(cleaned_data, **{'name':self.object.patent.name})

	def form_valid(self, form):
		print form.cleaned_data
		if form.cleaned_data["action"] == u'submit':
			if PatentExpertRating.objects.filter(report=self.object, submit_date=None):
				messages.error(self.request, u'提交失败：专家评价未全部完成')
				return super(PatentReportDetailView, self).form_invalid(form)
			if PatentExpertRating.objects.filter(report=self.object, ratings="-1"):
				messages.error(self.request, u'提交失败：存在未处理的拒绝评价')
				return super(PatentReportDetailView, self).form_invalid(form)
			self.success_message = u'专利"%(name)s"评级提交成功'
			self.success_url = reverse_lazy('patent-package-detail', args=(self.object.package.pk,))
		elif form.cleaned_data["action"] == u'save':
			self.success_message = u'评级草稿保存成功'
			self.success_url = reverse_lazy('patent-report-detail', args=(self.object.package.pk, self.object.pk))
		return super(PatentReportDetailView, self).form_valid(form)

	def form_invalid(self, form):
		error_msg = u'信息更新失败'
		messages.error(self.request, error_msg)
		return super(PatentReportDetailView, self).form_invalid(form)
