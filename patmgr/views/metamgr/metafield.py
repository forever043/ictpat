# coding=utf-8
from django.http import HttpResponse
from django.db.models import Q
from libs.django_datatables_view.base_datatable_view import BaseDatatableView

from patmgr.models import PatentType

class PatentMetaJson(BaseDatatableView):
	columns = ['pk', 'name', 'sort', 'pk', 'DT_RowId']
	max_display_length = 500

	def filter_queryset(self, qs):
		sSearch = self.request.GET.get('sSearch', None)
		if sSearch:
			qs = qs.filter(Q(name__icontains=sSearch))
		return qs

	def render_column(self, row, column):
		if column == 'DT_RowId':
			return '%d' % (row.pk)
		return super(PatentMetaJson, self).render_column(row, column)

	def get_context_data(self, *args, **kwargs):
		# not a POST, super take care of it
		if self.request.method != "POST":
			return super(PatentMetaJson, self).get_context_data(*args, **kwargs);

		print self.request.POST
		pk = self.request.POST.get('pk', "-1")
		if pk == "-1":
			meta = self.model()
			meta.name = self.request.POST.get('name', '未命名')
			#ef.disabled = True;
			meta.sort = 100;
			meta.save();
			value = {column: self.render_column(meta, column) for column in self.get_columns()}
			ret = {'result': 'ok', 'value': value }
		else:
			column = self.columns[int(self.request.POST['column'])]
			value = self.request.POST.get('value', "NOValue")
			meta = self.model.objects.all().get(pk=pk)
			setattr(meta, column, value)
			meta.save(update_fields=[column])
			ret = {'result': 'ok', 'value': value}
		return ret;
		
