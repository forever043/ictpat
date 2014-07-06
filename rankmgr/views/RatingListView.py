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
import json

from rankmgr.models import PatentExpertRating

class PatentRatingListView(ListView):
	model = PatentExpertRating

	def get_context_data(self, **kwargs):
		context = super(PatentRatingListView, self).get_context_data(**kwargs)
		context['request'] = self.request
		context['submit_list'] = self.model.objects.filter(expert=self.request.user).exclude(submit_date=None).exclude(ratings="-1").order_by("report__package")
		context['reject_list'] = self.model.objects.filter(expert=self.request.user).exclude(submit_date=None).filter(ratings="-1").order_by("report__package")
		return context

	def get_queryset(self):
		object_list = self.model.objects.filter(expert=self.request.user, submit_date=None).exclude(report__package__submit_date=None).order_by("report__package")
		return object_list

