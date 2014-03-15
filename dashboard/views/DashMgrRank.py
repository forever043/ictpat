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

from patmgr.models import *
from patmgr.forms import *

class DashMgrRankView(SuccessMessageMixin, CreateView):
	#model = PatentRank
	#form_class = PatentRankForm
	#template_name = 'patmgr/patent_rank.html'
	#success_message = u'专利 "%(name)s" 评价成功'
	ref_model = None
	ref_name = ''
	error_message = u'"%(name)s" 评价失败'
	default_referer_url = '/'

	def get_context_data(self, **kwargs):
		context = super(DashMgrRankView, self).get_context_data(**kwargs)
		context['request'] = self.request

		if '__next__' in self.request.POST:
			context['i__next__'] = self.request.POST['__next__']
		else:
			if 'HTTP_REFERER' in self.request.META:
				context['i__next__'] = self.request.META['HTTP_REFERER']
			else:
				context['i__next__'] = self.default_referer_url

		pk = self.kwargs.get(self.pk_url_kwarg, None)
		context[self.ref_name] = self.ref_model.objects.get(pk=pk)

		return context

	def get_success_message(self, cleaned_data):
		pk = self.kwargs.get(self.pk_url_kwarg, None)
		refobject = self.ref_model.objects.get(pk=pk)
		return self.success_message % dict(cleaned_data, **{'name':refobject.name})

	def get_success_url(self):
		return self.request.POST['__next__']

	def get_initial(self):
		initial = {}

		pk = self.kwargs.get(self.pk_url_kwarg, None)
		refobject = self.ref_model.objects.get(pk=pk)
		expert = self.request.user

		try:
 			rank = self.model.objects.get((self.ref_name, refobject), expert=expert)
			initial['rank'] = rank.rank
			initial['remark'] = rank.remark
		except ObjectDoesNotExist:
			initial['remark'] = ""
		finally:
			initial[self.ref_name] = refobject
			initial['expert'] = expert
		return initial

	def form_invalid(self, form):
		error_msg = u'信息更新失败'
		messages.error(self.request, error_msg)
		return super(DashMgrRankView, self).form_invalid(form)
