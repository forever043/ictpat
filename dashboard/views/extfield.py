# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.db.models import Q
from libs.django_datatables_view.base_datatable_view import BaseDatatableView

class ExtFieldJson(BaseDatatableView):
	columns = ['field_label', 'field_name', 'retrieval', 'disabled', 'sort', 'pk', 'DT_RowId']
	max_display_length = 500

	def filter_queryset(self, qs):
		sSearch = self.request.GET.get('sSearch', None)
		if sSearch:
			qs = qs.filter(Q(field_name__icontains=sSearch)|Q(field_label__icontains=sSearch))
		return qs

	def render_column(self, row, column):
		if column == 'DT_RowId':
			return '%d' % (row.pk)
		return super(ExtFieldJson, self).render_column(row, column)

	def get_context_data(self, *args, **kwargs):
		# not a POST, super take care of it
		if self.request.method != "POST":
			return super(ExtFieldJson, self).get_context_data(*args, **kwargs);

		pk = self.request.POST.get('pk', "-1")
		if pk == "-1":
			ef = self.model()
			ef.field_name = self.request.POST.get('field_name', 'unnamed')
			ef.field_label = self.request.POST.get('field_label', '未命名属性')
			ef.retrieval = False;
			ef.disabled = True;
			ef.sort = 100;
			ef.save();
			value = {column: self.render_column(ef, column) for column in self.get_columns()}
			ret = {'result': 'ok', 'value': value }
		else:
			column = self.columns[int(self.request.POST['column'])]
			value = self.request.POST.get('value', "NOValue")
			ef = self.model.objects.all().get(pk=pk)
			setattr(ef, column, value)
			ef.save(update_fields=[column])
			ret = {'result': 'ok', 'value': value}
		return ret;
		
