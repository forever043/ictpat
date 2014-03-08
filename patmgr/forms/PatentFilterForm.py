# coding=utf-8
from django import forms

from patmgr.models import *

class PatentFilterForm(forms.Form):
	name = forms.CharField(max_length=128, label='专利名称', required=False, 
			widget=forms.TextInput(attrs={'class':'text-input large-input'}))
	department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="(所有部门)", label="所属部门")
	inventors = forms.CharField(max_length=256, label='发明人',required=False, 
			widget=forms.TextInput(attrs={'class':'text-input large-input'}))
	type = forms.ModelChoiceField(queryset=PatentType.objects.all(), required=False, empty_label='(全部)', label="专利类型")
	state = forms.ModelChoiceField(queryset=PatentState.objects.all(), required=False, empty_label='(全部)', label='专利状态')
	apply_code = forms.CharField(max_length=20, label='申请号',required=False, 
			widget=forms.TextInput(attrs={'class':'text-input large-input'}))
	apply_date = forms.DateField(label='申请时间',required=False, 
			widget=forms.TextInput(attrs={'class':'text-input large-input datepicker'}))
	authorize_code = forms.CharField(max_length=20, required=False, label='授权号',
			widget=forms.TextInput(attrs={'class':'text-input large-input'}))
	authorize_date = forms.DateField(label='授权时间',required=False, 
			widget=forms.TextInput(attrs={'class':'text-input large-input datepicker'}))

