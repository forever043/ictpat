# coding=utf-8
from django import forms
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from  patmgr.models import Patent
from rankmgr.models import PatentPackage, PatentRatingReport, PatentExpertRating


class PatentRatingReportForm(forms.ModelForm):
    action = forms.CharField(widget=forms.HiddenInput(), initial="save")

    class Meta:
        model = PatentRatingReport
        fields = ['rating', 'rank', 'report', 'finish_date']
        widgets = {
            'rating': forms.HiddenInput(),
            'rank': forms.HiddenInput(),
            'report': forms.Textarea(attrs={'class': 'text-input large-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(PatentRatingReportForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.finish_date:
            self.fields['report'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        if self.cleaned_data["action"] == "submit":
            self.instance.finish_date = datetime.now()
        else:
            self.instance.finish_date = None
        instance = super(PatentRatingReportForm, self).save(commit)
        return instance


class PatentBriefForm(forms.ModelForm):
    class Meta:
        model = Patent
        fields = ['brief']
        widgets = {
            'brief': forms.Textarea(attrs={'class': 'text-input large-input'}),
        }