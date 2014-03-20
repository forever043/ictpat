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

class RetrvSchemeExport(View):
	model = None
	extfield_model = None
	ref_name = 'ref'
	builtin_field_model = None
	customized_field_model = None
	retrv_model = None
	retrv_field_model = None
	return_url = reverse_lazy('patent-retrvscheme')

	def get(self, *args, **kwargs):
		try:
			# Delete old RetrvScheme, clear data
			db.delete_table(self.retrv_model._meta.db_table)
			self.retrv_field_model.objects.all().delete()

			# Add builtin field
			for field in self.builtin_field_model.objects.filter(scheme__current=True).order_by('sort'):
				self.retrv_field_model(
					field_name = field.field_name,
					field_label = self.model._meta.get_field(field.field_name).verbose_name,
					display = field.display,
					retrieve = field.retrieve,
					type = field.type,
					sort = field.sort).save()
			for field in self.customized_field_model.objects.filter(scheme__current=True).order_by('sort'):
				self.retrv_field_model(
					field_name = field.field.field_name,
					field_label = field.field.field_label,
					display = field.display,
					retrieve = field.retrieve,
					type = field.type,
					sort = field.sort).save()

			# Recreate self.retrv_model table
			fields = [(f.name, f) for f in self.retrv_model._meta.local_fields]
			db.create_table(self.retrv_model._meta.db_table, fields)
			db.execute_deferred_sql()

			# Export Data
			for obj in self.model.objects.all():
				target = self.retrv_model()
				for field in self.builtin_field_model.objects.filter(scheme__current=True).order_by('sort'):
					setattr(target, field.field_name, getattr(obj, field.field_name))
				for extfield in self.extfield_model.objects.filter((self.ref_name, obj)):
					if hasattr(target, extfield.type.field_name):
						setattr(target, extfield.type.field_name, extfield.value)
				print target
				target.save()
		except:
			#db.rollback_transaction()
			messages.error(self.request, u"导出失败")
			return HttpResponseRedirect(self.retrun_url)

		messages.success(self.request, u"成功导出%d条记录至检索系统"%self.model.objects.all().count())
		return HttpResponseRedirect(self.return_url)

