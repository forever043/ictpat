# coding=utf-8
from django import forms
from django.utils import timezone
from libs.multiform import MultiModelForm

from patmgr.models import *


class PatentImportForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea(attrs={'class': 'text-area', 'rows':'20'}))

class UploadXlsxFileForm(forms.Form):
	#DB_CHOICES = [('P', '专利'), ('S', '软件')]
	#import_db = forms.ChoiceField(widget=forms.RadioSelect, choices=DB_CHOICES, initial='P', label='数据库')
	#import_type = forms.ChoiceField(widget=forms.RadioSelect, choices=TYPE_CHOICES, initial='A', label='导入类型')
	file = forms.FileField(label='请选择要导入的数据文件')

class MatchFieldForm(forms.Form):
	MATCH_SCHEMA_CHOICES = [
		('C', '使用自定义映射格式'),
		('P', '使用预定义映射格式')]
	TYPE_CHOICES = [
		('A', '增量：数据文件中的数据会追加到系统中，已存在的数据将会被更新'),
		('U', '更新：仅更新系统中存在的数据（通过专利申请号区分不同专利）'),
		('R', '覆盖：清空系统数据，并重新从数据文件中导入（请谨慎使用该功能）') ]

	import_type = forms.ChoiceField(widget=forms.RadioSelect, choices=TYPE_CHOICES, initial='A', label='导入类型')
	exclude_head = forms.BooleanField(label='忽略首行', required=False)
	match_schema_type = forms.ChoiceField(widget=forms.RadioSelect, choices=MATCH_SCHEMA_CHOICES, initial='C', label='映射格式')
	match_schema = forms.ChoiceField(label='预定义映射格式', required=False)

	name = forms.ChoiceField(label="专利名称")
	department = forms.ChoiceField(label="所属部门")
	inventors = forms.ChoiceField(label="发明人")
	type = forms.ChoiceField(label="专利类型")
	state = forms.ChoiceField(label='专利状态')
	apply_code = forms.ChoiceField(label='申请号')
	apply_date = forms.ChoiceField(label='申请时间')
	authorize_code = forms.ChoiceField(label='授权号')
	authorize_date = forms.ChoiceField(label='授权时间')

	extfields = {}
	basefields = {}
	FIELD_CHOICES = []

	def __init__(self, *args, **kwargs):
		colname_list = kwargs.pop('colname_list')
		super(MatchFieldForm, self).__init__(*args, **kwargs)

		self.FIELD_CHOICES = [('', '不导入')]
		for colid in range(0, len(colname_list)):
			self.FIELD_CHOICES.append((colid, colname_list[colid]))

		self.basefields = {}
		for (fieldname, item) in self.fields.items():
			if fieldname not in ['exclude_head', 'match_schema', 'import_type', 'match_schema_type']:
				item.choices = self.FIELD_CHOICES
				self.basefields[fieldname] = item

		self.extfields = {}
		extfield_list = PatentExtFieldType.objects.all()
		for extfield in extfield_list:
			self.fields[extfield.field_name] = forms.ChoiceField(required = False,
				label = extfield.field_label, choices=self.FIELD_CHOICES)
			self.extfields[extfield.field_name] = self.fields[extfield.field_name]

	def get_basefields(self):
		for fieldname in self.basefields:
			yield self[fieldname]

	def get_extfields(self):
		for fieldname in self.extfields:
			yield self[fieldname]

