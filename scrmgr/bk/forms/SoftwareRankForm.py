# coding=utf-8
from django import forms
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from scrmgr.models import SoftwareRank

class SoftwareRankForm(forms.ModelForm):
	class Meta:
		model = SoftwareRank
		fields = [ 'patent', 'expert', 'rank', 'remark' ]
		RATING_CHOICES = ((1,1), (2,2), (3,3), (4,4), (5,5),)
		widgets = {
			'patent': forms.HiddenInput(),
			'expert': forms.HiddenInput(),
			'rank': forms.RadioSelect(attrs={'class':'star'}, choices=RATING_CHOICES),
			'remark': forms.Textarea(attrs={'class':'text-input large-input'}),
		}

