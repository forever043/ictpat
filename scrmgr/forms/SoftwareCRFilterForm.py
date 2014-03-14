# coding=utf-8
from django import forms

from patmgr.models import Department
from scrmgr.models import *

class SoftwareCRFilterForm(forms.Form):
	name = forms.CharField(max_length=128, label=u'软件名称', required=False, 
			widget=forms.TextInput(attrs={'class':'text-input large-input'}))
	department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="(所有部门)", label="所属部门")
	developers = forms.CharField(max_length=256, label=u'发明人',required=False, 
			widget=forms.TextInput(attrs={'class':'text-input large-input'}))
	authorize_code = forms.CharField(max_length=20, required=False, label=u'软件登记号',
			widget=forms.TextInput(attrs={'class':'text-input large-input'}))
	authorize_date = forms.DateField(label=u'发证日期',required=False, 
			widget=forms.TextInput(attrs={'class':'text-input large-input datepicker'}))

