# coding=utf-8
from django import forms

from patmgr.models import Department
from scrmgr.models import *

class SoftwareCRFilterForm(forms.Form):
	name = forms.CharField(max_length=128, label=u'软件名称', required=False, 
			widget=forms.TextInput(attrs={'class':'text-input large-input'}))
	department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="(所有部门)", label="所属部门")
	inventors = forms.CharField(max_length=256, label=u'发明人',required=False, 
			widget=forms.TextInput(attrs={'class':'text-input large-input'}))
	type = forms.ModelChoiceField(queryset=SoftwareCRType.objects.all(), required=False, empty_label=u'(全部)', label="软件类型")
	state = forms.ModelChoiceField(queryset=SoftwareCRState.objects.all(), required=False, empty_label=u'(全部)', label=u'软件状态')
	apply_code = forms.CharField(max_length=20, label=u'申请号',required=False, 
			widget=forms.TextInput(attrs={'class':'text-input large-input'}))
	apply_date = forms.DateField(label=u'申请时间',required=False, 
			widget=forms.TextInput(attrs={'class':'text-input large-input datepicker'}))
	authorize_code = forms.CharField(max_length=20, required=False, label=u'授权号',
			widget=forms.TextInput(attrs={'class':'text-input large-input'}))
	authorize_date = forms.DateField(label=u'授权时间',required=False, 
			widget=forms.TextInput(attrs={'class':'text-input large-input datepicker'}))

