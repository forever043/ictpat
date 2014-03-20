# -*- coding: UTF-8 -*-
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib import messages
import os
import string
import datetime
import xlrd

class ImportWizardView(SessionWizardView):
	model = None
	form_list = []
	template_list = {}
	file_storage = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'uploads'))
	initial_dict = {
		"matchfield":	{
				"department": "0",
				"name":	"1",
				"inventors": "2",
				"apply_code": "3",
				"apply_date": "4",
				"state": "5",
				"authorize_code": "6",
				"authorize_date": "7",
				"type": "9",
		},
	}
	return_url = reverse_lazy('patent-import')

	def get_context_data(self, **kwargs):
		context = super(ImportWizardView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def get_template_names(self):
		return [self.template_list[self.steps.current]]

	def process_step_files(self, form):
		files = self.get_form_step_files(form)
		if self.steps.current == 'db_select':
			xlsfile = xlrd.open_workbook(file_contents = files['db_select-file'].read())
			table = xlsfile.sheets()[0]
			colname_list = []
			for colid in range(0,table.ncols-1):
				colname_list.append(xlrd.colname(colid))
			preview_list = []
			for rowid in range(0, 5):
				row = self.get_row_values(cell_list=[table.cell(rowid, colid) for colid in range(0,table.ncols-1)],
									 datemode = xlsfile.datemode)
				preview_list.append(row)
			self.storage.extra_data['colname_list'] = colname_list
			self.storage.extra_data['preview_list'] = preview_list
		return files

	def get_row_values(self, cell_list, datemode):
		row_values = []
		for cell in cell_list:
			if cell.ctype == xlrd.XL_CELL_DATE:
				row_values.append(datetime.datetime(*xlrd.xldate_as_tuple(cell.value, datemode)).strftime('%Y-%m-%d'))
			else:
				row_values.append(cell.value)
		return row_values

	def get_form_kwargs(self, step):
		if step == "matchfield":
			return {'colname_list': self.storage.extra_data.get('colname_list', []),}
		return {}

	def get_form_initial(self, step):
		return self.initial_dict.get(step, {})

	def done(self, form_list, **kwargs):
		cd = self.get_all_cleaned_data()
		matchfield_form = form_list[self.get_step_index('matchfield')]

		import_type = cd['import_type']
		exclude_head = cd['exclude_head']
		basefields = matchfield_form.basefields
		extfields = matchfield_form.extfields
		field_matchid = {}
		for field in dict(basefields, **extfields):
			if cd[field]:
				field_matchid[field] = int(cd[field])

		# process xlsfile
		xlsfile = xlrd.open_workbook(file_contents = cd['file'].read())
		table = xlsfile.sheets()[0]
		rowstart = 1 if exclude_head else 0
		success_count = 0
		error_count = 0
		for rowid in range(rowstart, table.nrows-1):
			row_values = self.get_row_values(
								datemode = xlsfile.datemode,
								cell_list = [table.cell(rowid, colid) for colid in range(0,table.ncols-1)])
			if {
  				'A': lambda: self.do_append(row_values, basefields, extfields, field_matchid),		# Append
  				'U': lambda: self.do_update(row_values, basefields, extfields, field_matchid),		# Update
  				'R': lambda: self.do_replace(row_values, basefields, extfields, field_matchid),		# Replace
			}[import_type]():
				success_count += 1
			else:
				error_count += 1

		if success_count > 0:
			messages.success(self.request, u"导入成功%d条记录" % success_count)
		if error_count > 0:
			messages.error(self.request, u"导入失败%d条记录" % error_count)

		return HttpResponseRedirect(self.return_url)

	def do_append(self, row, basefields, extfields, field_matchid):
		entry = self.model()
		for bf in basefields:
			if bf in field_matchid:
				try:
					field = getattr(self.model, bf)
					value = field.get_queryset().get(name=string.strip(row[field_matchid[bf]]))
				except AttributeError:
					value = row[field_matchid[bf]]
					if isinstance(value, str):
						value = string.strip(value)
				except ObjectDoesNotExist:
					print "FAILED: ", string.strip(row[1]), bf, ": '", string.strip(row[field_matchid[bf]]), "'"
					return False
				setattr(entry, bf, value)
		try:
			entry.save()
		except:
			print "FAILED: SAVE: ", entry
			return False

		return True

	def do_update(self, row, basefields, extfields, field_matchid):
		entry = self.model()
		for bf in basefields:
			if bf in field_matchid:
				setattr(entry, bf, string.strip(row[field_matchid[bf]]))
		print entry

	def do_replace(self, row, basefields, extfields, field_matchid):
		entry = self.model()
		for bf in basefields:
			if bf in field_matchid:
				setattr(entry, bf, string.strip(row[field_matchid[bf]]))
		print entry

