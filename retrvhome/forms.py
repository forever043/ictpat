# coding=utf-8
from django import forms

from retrvhome.models import *

class RetrvFilterForm(forms.Form):
	field_model = PatentField
	model = Patent

	def __init__(self, *args, **kwargs):
		super(RetrvFilterForm, self).__init__(*args, **kwargs)
		self.retrvfields = {}

		retrvfield_list = self.field_model.objects.filter(retrieve=True).order_by('sort')
		for field in retrvfield_list:
			if field.type == "OP":
				choices = [('', u'===== (全部) ====='),]
				choices.extend([(choice[field.field_name], choice[field.field_name])
									for choice in self.model.objects.values(field.field_name).distinct()])
				self.fields[field.field_name] = forms.ChoiceField(
					label = field.field_label,
					choices = choices,
					required = False)
			else: #field.type == "IN":
				self.fields[field.field_name] = forms.CharField(
					label = field.field_label,
					required = False,
					widget = forms.TextInput(attrs={'class': 'text-input large-input', 'autocomplete': 'off'}))


class SoftwareCRRetrvFilterForm(RetrvFilterForm):
	field_model = RetrvSoftwareCRField
	model = RetrvSoftwareCR

class PatentRetrvFilterForm(RetrvFilterForm):
	field_model = PatentField
	model = Patent

