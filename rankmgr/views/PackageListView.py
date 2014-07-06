# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import *
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.core import exceptions

from rankmgr.models import *

class PatentPackageListView(ListView):
	model = PatentPackage
	columns = [ 'name', 'count', 'state', 'submit_date', 'finish_date' ]

	def get_context_data(self, **kwargs):
		context = super(PatentPackageListView, self).get_context_data(**kwargs)
		context['request'] = self.request
		package_list = []
		for o in self.object_list:
			package_list.append((o, {
				'count':         PatentRatingReport.objects.filter(package=o).count(),
				'report_finish': PatentRatingReport.objects.filter(package=o).filter(finish_date__gt="1900-01-01").count(),
				'report_total' : PatentRatingReport.objects.filter(package=o).count(),
				'rating_finish': PatentExpertRating.objects.filter(report__package=o).filter(submit_date__gt="1900-01-01").count(),
				'rating_total' : PatentExpertRating.objects.filter(report__package=o).count(),
			}))
		context[self.context_object_name] = package_list
		return context

