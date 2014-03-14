# coding=utf-8
from django import forms
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from scrmgr.models import *

class SoftwareCRForm(forms.ModelForm):
	class Meta:
		model = SoftwareCR
		fields = [ 'department', 'name', 'developers', 'release_date', 'version',
				'authorize_code', 'authorize_date', 'authorize_file' ]
		widgets = {
			'name': forms.TextInput(attrs={'class':'text-input large-input'}),
			'developers': forms.TextInput(attrs={'class':'text-input large-input'}),
			'release_date': forms.TextInput(attrs={'class':'text-input large-input datepicker'}),
			'version': forms.TextInput(attrs={'class':'text-input large-input'}),
			'authorize_code': forms.TextInput(attrs={'class':'text-input large-input'}),
			'authorize_date': forms.TextInput(attrs={'class':'text-input large-input datepicker'}),
		}
		#error_messages= {}
		#initial

	def __init__(self, *args, **kwargs): 
		super(SoftwareCRForm, self).__init__(*args, **kwargs) 
		self.fields["department"].empty_label = "请选择软件所属部门..."
		#self.fields["apply_date"].value = timezone.now()

class SoftwareCRExtForm(SoftwareCRForm):
	extfields = {}

	def __init__(self, *args, **kwargs):
		super(SoftwareCRExtForm, self).__init__(*args, **kwargs)
		self.extfields = {}
		extfield_list = SoftwareCRExtFieldType.objects.filter(disabled=False).order_by('sort')
		for extfield in extfield_list:
			self.fields[extfield.field_name] = forms.CharField(
				label = extfield.field_label,
				required = False,
				widget = forms.TextInput(attrs={'class': 'text-input large-input'}))
			self.extfields[extfield.field_name] = self.fields[extfield.field_name]

	def get_extfields(self):
		for fieldname in self.extfields:
			yield self[fieldname]

	def save(self, commit=True):
		instance = super(SoftwareCRExtForm, self).save(commit)
		for extfield in self.extfields:
			extfield_type = SoftwareCRExtFieldType.objects.get(field_name=extfield)
			try:
				SoftwareCRExtField.objects.get(scr = instance, type = extfield_type)
				SoftwareCRExtField.objects.filter(scr = instance, type = extfield_type).update(value=self.cleaned_data[extfield])
			except ObjectDoesNotExist:
				ex = SoftwareCRExtField(scr = instance,
						    type = extfield_type,
						    value = self.cleaned_data[extfield])
				ex.save(commit)
		return instance

