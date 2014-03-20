# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import *
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from django.core import exceptions
from south.db import db
import json

from retrvhome.models import PatentField as RetrvPatentField
from retrvhome.models import Patent as RetrvPatent

class RetrvSchemeView(FormView):
	scheme_model = None
	builtinfield_model = None
	customizedfield_model = None

	def get_context_data(self, **kwargs):
		context = super(RetrvSchemeView, self).get_context_data(**kwargs)
		context['request'] = self.request
		context['scheme_list'] = self.scheme_model.objects.all()
		context['builtin_fields'] = self.builtinfield_model.objects.all()
		context['customized_fields'] = self.customizedfield_model.objects.all()
		return context

	def get_success_message(self, cleaned_data):
		return u'保存成功'

	def form_valid(self, form):
		return super(RetrvSchemeView, self).form_valid(form)

