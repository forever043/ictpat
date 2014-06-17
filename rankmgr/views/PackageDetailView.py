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
		self.object.expert_list   = [o.expert for o in PatentExpertRating.objects.filter(patent__package = self.object)]
		self.object.patent_count  = PatentRatingReport.objects.filter(package=self.object).count()
		self.object.rating_finish = PatentExpertRating.objects.filter(package=self.object).filter(submit_date__gt="1900-01-01").count()
 		self.object.rating_total  = PatentExpertRating.objects.filter(package=self.object).count()
		self.object.report_finish = PatentRatingReport.objects.filter(package=self.object).filter(finish_date__gt="1900-01-01").count()
		self.object.report_total  = PatentRatingReport.objects.filter(package=self.object).count()
		# Prepare patent list
		rating_list = PatentExpertRating.objects.filter(patent__package=self.object).order_by("patent", "expert")
		for o in rating_list:
			o.patent.rating_finish = PatentExpertRating.objects.filter(patent=o.patent).filter(submit_date__gt="1900-01-01").count()
			o.patent.rating_total = PatentExpertRating.objects.filter(patent=o.patent).count()
		context['rating_list'] = rating_list
		return context

