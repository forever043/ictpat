# -*- coding: UTF-8 -*-
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import *
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.core import exceptions
import json

class DashMgrRatingExpertAdd(View):
	model = None
	def dispatch(self, *args, **kwargs):
		# Only ajax request support
		if not self.request.is_ajax():
			raise Http404;
		response_data = {"result": "ok"}
		return HttpResponse(json.dumps(response_data),
			content_type="application/json")

class DashMgrRatingExpertDel(View):
	model = None
	def dispatch(self, *args, **kwargs):
		# Only ajax request support
		if not self.request.is_ajax():
			raise Http404;
		response_data = {"result": "ok"}
		return HttpResponse(json.dumps(response_data),
			content_type="application/json")

