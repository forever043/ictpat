# coding=utf-8
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

from scrmgr.models import *
from scrmgr.forms import *

class SCRRankView(SuccessMessageMixin, CreateView):
	model = SoftwareRank
	form_class = SoftwareRankForm
	template_name = 'scrmgr/scr_rank.html'
	success_message = u'软件 "%(name)s" 评价成功'
	error_message = u'软件 "%(name)s" 评价失败'

	def get_context_data(self, **kwargs):
		context = super(SoftwareRankView, self).get_context_data(**kwargs)
		context['request'] = self.request

		if '__next__' in self.request.POST:
			context['i__next__'] = self.request.POST['__next__']
		else:
			if 'HTTP_REFERER' in self.request.META:
				context['i__next__'] = self.request.META['HTTP_REFERER']
			else:
				context['i__next__'] = reverse_lazy('scr-list')

		pk = self.kwargs.get(self.pk_url_kwarg, None)
		context['scr'] = Software.objects.get(pk=pk)

		return context

	def get_success_message(self, cleaned_data):
		pk = self.kwargs.get(self.pk_url_kwarg, None)
		scr = Software.objects.get(pk=pk)
		return self.success_message % dict(cleaned_data, **{'name':scr.name})

	def get_success_url(self):
		return self.request.POST['__next__']

	def get_initial(self):
		initial = {}

		pk = self.kwargs.get(self.pk_url_kwarg, None)
		scr = Software.objects.get(pk=pk)
		expert = self.request.user

		try:
 			rank = SoftwareRank.objects.get(scr=scr, expert=expert)
			initial['rank'] = rank.rank
			initial['remark'] = rank.remark
		except ObjectDoesNotExist:
			initial['remark'] = ""
		finally:
			initial['scr'] = scr
			initial['expert'] = expert
		return initial

	def form_invalid(self, form):
		error_msg = u'信息更新失败'
		messages.error(self.request, error_msg)
		return super(SoftwareRankView, self).form_invalid(form)
