# coding=utf-8
from django import forms
from django.utils import timezone

from patmgr.models import RetrvScheme
from patmgr.models import BuiltinRetrvField
from patmgr.models import CustomizedRetrvField

class PatentRetrvSchemeForm(forms.ModelForm):
	class Meta:
		model = RetrvScheme
		fields = [ 'name' ]

