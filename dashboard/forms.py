# coding=utf-8
from django import forms
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from dashboard.models import ExpertProfile


class ExpertProfileForm(forms.ModelForm):
    repeat_passwd = forms.CharField(widget=forms.PasswordInput(attrs={'class':'text-input large-input'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    organization = forms.CharField(widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    research_field = forms.CharField(widget=forms.TextInput(attrs={'class':'text-input large-input'}))

    class Meta:
        model = User

    def save(self, commit=True):
        instance = super(ExpertProfileForm, self).save(commit)
        return instance

