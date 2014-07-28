# coding=utf-8
from django import forms
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from dashboard.models import ExpertProfile


class ExpertProfileForm(UserCreationForm):
    first_name     = forms.CharField(label=u'名字', widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    last_name      = forms.CharField(label=u'姓氏', widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    email          = forms.EmailField(label=u"E-Mail", widget=forms.EmailInput(attrs={'class':'text-input large-input'}))
    phone          = forms.CharField(label=u'联系电话', widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    organization   = forms.CharField(label=u'工作单位', widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    research_field = forms.CharField(label=u'研究领域', widget=forms.Textarea(attrs={'class':'text-input large-input'}))

    username = forms.RegexField(label=u"用户名", max_length=30, regex=r'^[\w.@+-]+$',
                                widget=forms.PasswordInput(attrs={'class':'text-input large-input'}))
    password1 = forms.CharField(label=u"密码", widget=forms.PasswordInput(attrs={'class':'text-input large-input'}))
    password2 = forms.CharField(label=u"确认密码", widget=forms.PasswordInput(attrs={'class':'text-input large-input'}))

    def save(self, commit=True):
        user = super(ExpertProfileForm, self).save(False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            user.expertprofile = ExpertProfile(
                user=user,
                phone=self.cleaned_data["phone"],
                organization = self.cleaned_data["organization"],
                research_field = self.cleaned_data["research_field"])
            user.expertprofile.save()
            user.groups.add(Group.objects.filter(name=u'评审专家').first())
            user.save()

        return user
