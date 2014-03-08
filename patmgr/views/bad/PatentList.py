# coding=utf-8
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.core import exceptions
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError, DatabaseError
from django.views.generic.edit import FormMixin
from endless_pagination.views import AjaxListView
import json

from patmgr.models import *
from patmgr.forms import *

class PatentAjaxListView(AjaxListView):
	model = Patent
	context_object_name = 'patent_list'
	template_name = 'patmgr/list_patent_ajax.html'
	page_template = 'patmgr/list_patent_page.html'

	def get_context_data(self, **kwargs):
		context = super(PatentAjaxListView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

