# coding=utf-8
from django import forms

from retrvhome.models import *

class RetrvFilterForm(forms.Form):
	model = PatentField

	def __init__(self, *args, **kwargs):
		super(RetrvFilterForm, self).__init__(*args, **kwargs)
		self.retrvfields = {}

		retrvfield_list = self.model.objects.filter(retrieve=True).order_by('sort')
		for field in retrvfield_list:
			self.fields[field.field_name] = forms.CharField(
				label = field.field_label,
				required = False,
				widget = forms.TextInput(attrs={'class': 'text-input large-input'}))

