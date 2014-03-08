# coding=utf-8
from django.http import HttpResponse
from django.db.models import Q
from libs.django_datatables_view.base_datatable_view import BaseDatatableView

from patmgr.models import Patent

class PatentListJson(BaseDatatableView):
	model = Patent
	columns = ['department', 'name', 'inventors', 'apply_code', 'apply_date', 'authorize_code', 'pk', 'DT_RowId']
	#order_columns = ['field_label', 'field_name', '', '', 'sort', 'pk', 'pk']
	max_display_length = 2000

	def filter_queryset(self, qs):
		sSearch = self.request.GET.get('sSearch', None)
		if sSearch:
			qs = qs.filter(Q(name__icontains=sSearch))
		return qs

	def render_column(self, row, column):
		if column == 'DT_RowId':
			return '%d' % (row.pk)
		elif column == 'department':
			return row.department.name
		elif column == 'authorize_code':
			if row.authorize_code != "":
				return row.authorize_code
			else:
				return row.state.name
		return super(PatentListJson, self).render_column(row, column)

