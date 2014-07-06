# -*- coding: UTF-8 -*-
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import *
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.core import exceptions
from datetime import datetime
import json

from django.contrib.auth.models import User
from rankmgr.models import PatentPackage, PatentRatingReport, PatentExpertRating

class DashMgrRatingExpertAdd(View):
	model = None
	def dispatch(self, *args, **kwargs):
		# Only ajax request support
		if not self.request.is_ajax():
			raise Http404;
		try:
			report = PatentRatingReport.objects.get(pk=self.request.GET.get("patent"))
			expert = User.objects.get(pk=self.request.GET.get("expert"))
			PatentExpertRating(report=report, expert=expert).save()
			response_data = {"result": "ok"}
		except:
			response_data = {"result": "err"}

		return HttpResponse(json.dumps(response_data),
			content_type="application/json")

class DashMgrRatingExpertDel(View):
	model = None
	def dispatch(self, *args, **kwargs):
		# Only ajax request support
		if not self.request.is_ajax():
			raise Http404;
		try:
			report = PatentRatingReport.objects.get(pk=self.request.GET.get("patent"))
			expert = User.objects.get(pk=self.request.GET.get("expert"))
			PatentExpertRating.objects.get(report=report, expert=expert).delete()
			response_data = {"result": "ok"}
		except:
			response_data = {"result": "err"}

		return HttpResponse(json.dumps(response_data),
			content_type="application/json")

class DashMgrRatingPackageSubmit(SuccessMessageMixin, View):
	return_url = "/"
	def dispatch(self, *args, **kwargs):
		try:
			pkg = PatentPackage.objects.get(pk=kwargs['pk'])
		except:
			raise Http404;

		try:
			PatentPackage.objects.filter(pk=kwargs['pk']).update(submit_date=datetime.now())
			messages.success(self.request, u"专利包\"%s\"提交成功" % pkg.name)
		except:
			messages.error(self.request, u"专利包\"%s\"提交失败，请重试或与管理员联系" % pkg.name)

		return HttpResponseRedirect(self.return_url)

