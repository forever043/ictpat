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

from scrmgr.forms import *
from scrmgr.models import *

from retrvhome.models import SoftwareField as RetrvSoftwareField
from retrvhome.models import Software as RetrvSoftware

class SCRRetrvSchemeView(FormView):
	template_name = 'scrmgr/retrvmgr.html'
	form_class = SoftwareRetrvSchemeForm
	success_url = reverse_lazy('scr-retrvscheme')

	def get_context_data(self, **kwargs):
		context = super(SoftwareRetrvSchemeView, self).get_context_data(**kwargs)
		context['request'] = self.request
		context['scheme_list'] = RetrvScheme.objects.all()
		return context

	def get_success_message(self, cleaned_data):
		return u'保存成功'

	def form_valid(self, form):
		return super(SoftwareRetrvSchemeView, self).form_valid(form)

class RetrvSchemeExport(View):
	def get(self, *args, **kwargs):
		try:
			db.start_transaction()

			# Delete old RetrvScheme, clear data
			db.delete_table(RetrvSoftware._meta.db_table)
			RetrvSoftwareField.objects.all().delete()

			# Add builtin field
			for field in BuiltinRetrvField.objects.filter(scheme__current=True).order_by('sort'):
				RetrvSoftwareField(
					field_name = field.field_name,
					field_label = Software._meta.get_field(field.field_name).verbose_name,
					display = field.display,
					retrieve = field.retrieve,
					sort = field.sort).save()
			for field in CustomizedRetrvField.objects.filter(scheme__current=True).order_by('sort'):
				RetrvSoftwareField(
					field_name = field.field.field_name,
					field_label = field.field.field_label,
					display = field.display,
					retrieve = field.retrieve,
					sort = field.sort).save()

			# Recreate RetrvSoftware table
			fields = [(f.name, f) for f in RetrvSoftware._meta.local_fields]
			db.create_table(RetrvSoftware._meta.db_table, fields)
			db.execute_deferred_sql()

			# Export Softwares
			for scr in Software.objects.all():
				target = RetrvSoftware()
				for field in BuiltinRetrvField.objects.filter(scheme__current=True).order_by('sort'):
					setattr(target, field.field_name, getattr(scr, field.field_name))
				for extfield in SoftwareExtField.objects.filter(scr=scr):
					if hasattr(target, extfield.type.field_name):
						setattr(target, extfield.type.field_name, extfield.value)
				print target
				target.save()

			# Commit transaction
			db.commit_transaction()
		except:
			db.rollback_transaction()
			return HttpResponse('Failed')

		return HttpResponse('OK')

