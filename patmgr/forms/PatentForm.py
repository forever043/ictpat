# coding=utf-8
from django import forms
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from patmgr.models import *


class PatentForm(forms.ModelForm):
    rank_file = forms.FileField(required=False, label="专利评价文件")
    spec_file = forms.FileField(required=False, label="专利说明文件")
    class Meta:
        model = Patent
        fields = ['name', 'department', 'inventors', 'type', 'state', 'brief',
                  'apply_code', 'apply_date', 'authorize_code',
                  'authorize_date', 'apply_file', 'authorize_file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'text-input large-input'}),
            'inventors': forms.TextInput(attrs={'class': 'text-input large-input'}),
            'brief': forms.Textarea(attrs={'class': 'text-input large-input', 'rows': '20'}),
            'apply_code': forms.TextInput(attrs={'class': 'text-input large-input'}),
            'apply_date': forms.TextInput(attrs={'class': 'text-input large-input datepicker'}),
            'authorize_code': forms.TextInput(attrs={'class': 'text-input large-input'}),
            'authorize_date': forms.TextInput(attrs={'class': 'text-input large-input datepicker'}),
        }
    #error_messages= {}
    #initial

    def __init__(self, *args, **kwargs):
        super(PatentForm, self).__init__(*args, **kwargs)
        self.fields["type"].empty_label = None
        self.fields["state"].empty_label = None
        self.fields["department"].empty_label = "请选择专利所属部门..."
        #self.fields["apply_date"].value = timezone.now()

    def save(self, commit=True):
        pass



class PatentExtForm(PatentForm):
    extfields = {}

    def __init__(self, *args, **kwargs):
        super(PatentExtForm, self).__init__(*args, **kwargs)
        self.extfields = {}
        extfield_list = PatentExtFieldType.objects.filter(disabled=False).order_by('sort')
        for extfield in extfield_list:
            self.fields[extfield.field_name] = forms.CharField(
                label=extfield.field_label,
                required=False,
                widget=forms.TextInput(attrs={'class': 'text-input large-input'}))
            self.extfields[extfield.field_name] = self.fields[extfield.field_name]

    def get_extfields(self):
        for fieldname in self.extfields:
            yield self[fieldname]

    def save(self, commit=True):
        instance = super(PatentExtForm, self).save(commit)
        for extfield in self.extfields:
            extfield_type = PatentExtFieldType.objects.get(field_name=extfield)
            try:
                PatentExtField.objects.get(patent=instance, type=extfield_type)
                PatentExtField.objects.filter(patent=instance, type=extfield_type).update(
                    value=self.cleaned_data[extfield])
            except ObjectDoesNotExist:
                ex = PatentExtField(patent=instance,
                                    type=extfield_type,
                                    value=self.cleaned_data[extfield])
                ex.save(commit)
        return instance


class PatentExtentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        del kwargs['instance']
        super(PatentExtentForm, self).__init__(*args, **kwargs)

        extfield_list = PatentExtFieldType.objects.all()
        for extfield in extfield_list:
            self.fields[extfield.field_name] = forms.CharField(
                label=extfield.field_label,
                required=False,
                widget=forms.TextInput(attrs={'class': 'text-input large-input'}))

    def save(self, commit=True):
        print "PatentExtentForm.save()"
        for extfield in self.fields:
            print self.cleaned_data[extfield]


class PatentBatchAddForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'text-area', 'rows': '20'}))


class PatentEditForm(forms.Form):
    base_forms = {
        'basic': PatentForm,
        'extent': PatentExtentForm,
    }

    def save(self, commit=True):
        self.forms['extent'].save(commit)
        return self.forms['basic'].save(commit)


#class PatentFormBasic(forms.Form):
#    name = forms.CharField(max_length=128, label='专利名称',
#                           widget=forms.TextInput(attrs={'class': 'text-input large-input'}))
#    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="请选择专利所属部门...", label="所属部门")
#    inventors = forms.CharField(max_length=256, label='发明人',
#                                widget=forms.TextInput(attrs={'class': 'text-input large-input'}))
#    type = forms.ModelChoiceField(queryset=PatentType.objects.all(), empty_label=None, label="专利类型")
#    state = forms.ModelChoiceField(queryset=PatentState.objects.all(), empty_label=None, label='专利状态')
#    apply_code = forms.CharField(max_length=20, label='申请号',
#                                 widget=forms.TextInput(attrs={'class': 'text-input large-input'}))
#    apply_date = forms.DateField(label='申请时间',
#                                 widget=forms.TextInput(attrs={'class': 'text-input large-input datepicker'}))
#    apply_file = forms.FileField(required=False, label="专利受理证书")
#    authorize_code = forms.CharField(max_length=20, required=False, label='授权号',
#                                     widget=forms.TextInput(attrs={'class': 'text-input large-input'}))
#    authorize_date = forms.DateField(label='授权时间', required=False,
#                                     widget=forms.TextInput(attrs={'class': 'text-input large-input datepicker'}))
#    authorize_file = forms.FileField(required=False, label="专利授权证书")
## extfields = forms.ManyToManyField(PatentExtField, blank=True, null=True, label='扩展属性')
##ranks = forms.ManyToManyField(PatentRank, blank=True, null=True, label='评分')


#class PatentFormAdvance(forms.Form):
#    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'text-area', 'rows': '20'}))
