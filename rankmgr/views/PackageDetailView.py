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

from rankmgr.models import *

class PatentPackageDetailView(DetailView):
	model = PatentPackage
	default_referer_url = '/'

	def get_context_data(self, **kwargs):
		context = super(PatentPackageDetailView, self).get_context_data(**kwargs)
		context['request'] = self.request
		if '__next__' in self.request.POST:
			context['i__next__'] = self.request.POST['__next__']
		else:
			if 'HTTP_REFERER' in self.request.META:
				context['i__next__'] = self.request.META['HTTP_REFERER']
			else:
				context['i__next__'] = self.default_referer_url
		# Fill extra attributes
		self.object.expert_list   = {}.fromkeys([o.expert for o in PatentExpertRating.objects.filter(report__package = self.object).order_by('expert')]).keys()
		for o in self.object.expert_list:
			o.profile = o.get_profile()
		self.object.patent_count  = PatentRatingReport.objects.filter(package=self.object).count()
		self.object.rating_finish = PatentExpertRating.objects.filter(report__package=self.object).filter(submit_date__gt="1900-01-01").count()
 		self.object.rating_total  = PatentExpertRating.objects.filter(report__package=self.object).count()
		self.object.rating_percent = 100*self.object.rating_finish/self.object.rating_total
		self.object.report_finish = PatentRatingReport.objects.filter(package=self.object).filter(finish_date__gt="1900-01-01").count()
		self.object.report_total  = PatentRatingReport.objects.filter(package=self.object).count()
		self.object.report_percent = 100*self.object.report_finish / self.object.report_total
		# Prepare patent list
		rating_list = PatentExpertRating.objects.filter(report__package=self.object).order_by("report", "expert")
		for o in rating_list:
			o.report.rating_finish = PatentExpertRating.objects.filter(report=o.report).filter(submit_date__gt="1900-01-01").count()
			o.report.rating_total = PatentExpertRating.objects.filter(report=o.report).count()
		context['rating_list'] = rating_list
		return context

