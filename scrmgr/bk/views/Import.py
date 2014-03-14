import os
import string
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
import xlrd
from django.core.exceptions import ObjectDoesNotExist

from scrmgr.forms import *

FORMS = [
    #("import_config", SoftwareImportForm),
    ("db_select",     UploadXlsxFileForm),
    ("matchfield",    MatchFieldForm),
]

TEMPLATES = {
    "import_config": "scrmgr/import/import_config.html",
    "db_select":     "scrmgr/import/db_select.html",
    "matchfield":    "scrmgr/import/matchfield.html",
}

class SCRImportWizard(SessionWizardView):
	form_list = FORMS
	file_storage = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'uploads'))

	def get_context_data(self, **kwargs):
		context = super(SoftwareImportWizard, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def get_template_names(self):
		return [TEMPLATES[self.steps.current]]

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
				row = table.row_values(rowid)
				if row:
					preview_list.append(row)
			self.storage.extra_data['colname_list'] = colname_list
			self.storage.extra_data['preview_list'] = preview_list
		return files

	def get_form_kwargs(self, step):
		if step == "matchfield":
			return {'colname_list': self.storage.extra_data.get('colname_list', []),}
		return {}

	def done(self, form_list, **kwargs):
		cd = self.get_all_cleaned_data()
		matchfield_form = form_list[self.get_step_index('matchfield')]

		import_type = cd['import_type']
		exclude_head = cd['exclude_head']
		basefields = matchfield_form.basefields
		extfields = matchfield_form.extfields
		field_matchid = {}
		for field in dict(basefields, **extfields):
			if cd[field] != 'None':
				field_matchid[field] = int(cd[field])

		# process xlsfile
		xlsfile = xlrd.open_workbook(file_contents = cd['file'].read())
		table = xlsfile.sheets()[0]
		rowstart = 1 if exclude_head else 0
		for rowid in range(rowstart, table.nrows-1):
			{
  				'A': lambda: self.do_append(table.row_values(rowid), basefields, extfields, field_matchid),		# Append
  				'U': lambda: self.do_update(table.row_values(rowid), basefields, extfields, field_matchid),		# Update
  				'R': lambda: self.do_replace(table.row_values(rowid), basefields, extfields, field_matchid),	# Replace
			}[import_type]()

		return HttpResponseRedirect('/page-to-redirect-to-when-done/')

	def do_append(self, row, basefields, extfields, field_matchid):
		scr = Software()
		for bf in basefields:
			if bf in field_matchid:
				try:
					field = getattr(Software, bf)
					value = field.get_queryset().get(name=string.strip(row[field_matchid[bf]]))
				except AttributeError:
					value = row[field_matchid[bf]]
					if isinstance(value, str):
						value = string.strip(value)
				except ObjectDoesNotExist:
					print "FAILED: ", string.strip(row[1]), bf, ": '", string.strip(row[field_matchid[bf]]), "'"
					break
				setattr(scr, bf, value)

	def do_update(self, row, basefields, extfields, field_matchid):
		scr = Software()
		for bf in basefields:
			if bf in field_matchid:
				setattr(scr, bf, string.strip(row[field_matchid[bf]]))
		print scr

	def do_replace(self, row, basefields, extfields, field_matchid):
		scr = Software()
		for bf in basefields:
			if bf in field_matchid:
				setattr(scr, bf, string.strip(row[field_matchid[bf]]))
		print scr
