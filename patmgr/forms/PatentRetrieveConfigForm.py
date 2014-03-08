# coding=utf-8
from django import forms
from django.utils import timezone
from libs.multiform import MultiModelForm

from patmgr.models import Patent
from patmgr.models import Department
from patmgr.models import PatentType
from patmgr.models import PatentState


class PatentRetrieveConfigForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea(attrs={'class': 'text-area', 'rows':'20'}))

