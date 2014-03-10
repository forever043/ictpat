# coding=utf-8
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import *
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from django.core import exceptions
from south.db import db
import json

from patmgr.forms import *
from patmgr.models import *

from retrvhome.models import PatentField as RetrvPatentField
from retrvhome.models import Patent as RetrvPatent

class PatentRetrieveManager(FormView):
	template_name = 'patmgr/patlist.html'
	form_class = PatentRetrieveConfigForm
	success_url = reverse_lazy('patent-retvmgr')

	def get_context_data(self, **kwargs):
		context = super(PatentRetrieveManager, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def get_success_message(self, cleaned_data):
		return u'保存成功'

	def form_valid(self, form):
		return super(PatentRetrieveManager, self).form_valid(form)

class RetrvSchemeExport(View):
	def get(self, *args, **kwargs):
		db.delete_table(RetrvPatent._meta.db_table)
		RetrvPatentField.objects.all().delete()

		# Add builtin field
		for field in BuiltinRetrvField.objects.filter(scheme__current=True).order_by('sort'):
			RetrvPatentField(
				field_name = field.field_name,
				field_label = Patent._meta.get_field(field.field_name).verbose_name,
				display = field.display,
				retrieve = field.retrieve,
				sort = field.sort).save()
		for field in CustomizedRetrvField.objects.filter(scheme__current=True).order_by('sort'):
			RetrvPatentField(
				field_name = field.field.field_name,
				field_label = field.field.field_label,
				display = field.display,
				retrieve = field.retrieve,
				sort = field.sort).save()

		# Recreate RetrvPatent table
		fields = [(f.name, f) for f in RetrvPatent._meta.local_fields]
		db.create_table(RetrvPatent._meta.db_table, fields)

		# Export Patents
		for patent in Patent.objects.all():
			target = RetrvPatent()
			for field in BuiltinRetrvField.objects.filter(scheme__current=True).order_by('sort'):
				setattr(target, field.field_name, getattr(patent, field.field_name))
			for extfield in PatentExtField.objects.filter(patent=patent):
				if hasattr(target, extfield.type.field_name):
					setattr(target, extfield.type.field_name, extfield.value)
			print target
			target.save()

		return HttpResponse('OK')

