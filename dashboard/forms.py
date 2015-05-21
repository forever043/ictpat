# coding=utf-8
from django import forms
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from dashboard.models import ExpertProfile
from dashboard.models import ExpertCatalog


class ExpertProfileForm(UserCreationForm):
    first_name     = forms.CharField(label=u'名字', widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    last_name      = forms.CharField(label=u'姓氏', widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    email          = forms.EmailField(label=u"E-Mail", widget=forms.EmailInput(attrs={'class':'text-input large-input'}))
    phone          = forms.CharField(label=u'联系电话', widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    organization   = forms.CharField(label=u'工作单位', widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    research_field = forms.CharField(label=u'研究领域', widget=forms.Textarea(attrs={'class':'text-input large-input'}))

    username = forms.RegexField(label=u"用户名", max_length=30, regex=r'^[\w.@+-]+$',
                                widget=forms.TextInput(attrs={'class':'text-input large-input'}))
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
                research_field = self.cleaned_data["research_field"],
                catalog = ExpertCatalog.objects.get(id=1))
            user.expertprofile.save()
            user.groups.add(Group.objects.filter(name=u'评审专家').first())
            user.save()

        return user

class ExpertProfileEditForm(UserChangeForm):
    first_name     = forms.CharField(label=u'名字', widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    last_name      = forms.CharField(label=u'姓氏', widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    email          = forms.EmailField(label=u"E-Mail", widget=forms.EmailInput(attrs={'class':'text-input large-input'}))
    phone          = forms.CharField(label=u'联系电话', widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    organization   = forms.CharField(label=u'工作单位', widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    research_field = forms.CharField(label=u'研究领域', widget=forms.Textarea(attrs={'class':'text-input large-input'}))

    username = forms.RegexField(label=u"用户名", max_length=30, regex=r'^[\w.@+-]+$',
                                widget=forms.TextInput(attrs={'class':'text-input large-input'}))
    password1 = forms.CharField(label=u"密码", widget=forms.PasswordInput(attrs={'class':'text-input large-input'}))
    password2 = forms.CharField(label=u"确认密码", widget=forms.PasswordInput(attrs={'class':'text-input large-input'}))

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance and instance.pk:
            initial = kwargs.get('initial', {})
            initial['phone'] = instance.expertprofile.phone
            initial['organization'] = instance.expertprofile.organization
            initial['research_field'] = instance.expertprofile.research_field
            kwargs['initial'] = initial
        super(ExpertProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['last_login'].required = False
        self.fields['date_joined'].required = False
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def clean_last_login(self):
        return self.initial["last_login"]
    def clean_date_joined(self):
        return self.initial["date_joined"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u'密码不匹配')
        return password2

    def save(self, commit=True):
        user = super(ExpertProfileEditForm, self).save(True)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.expertprofile.phone=self.cleaned_data["phone"]
        user.expertprofile.organization = self.cleaned_data["organization"]
        user.expertprofile.research_field = self.cleaned_data["research_field"]
        if self.cleaned_data["password2"]:
            user.set_password(self.cleaned_data["password2"])
        if commit:
            user.is_active = True
            user.groups.add(Group.objects.filter(name=u'评审专家').first())
            user.expertprofile.save()
            user.save()
        return user
