# coding=utf-8
from django import forms
from django.utils import timezone

from scrmgr.models import RetrvScheme
from scrmgr.models import BuiltinRetrvField
from scrmgr.models import CustomizedRetrvField

class SoftwareRetrvSchemeForm(forms.ModelForm):
	class Meta:
		model = RetrvScheme
		fields = [ 'name' ]

