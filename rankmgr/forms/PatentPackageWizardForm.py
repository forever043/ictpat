# coding=utf-8
from django import forms
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from dashboard.models import ExpertCatalog
from rankmgr.models import RankCatalog, RankItem

class PatentPackageBaseInfoForm(forms.Form):
    name = forms.CharField(label=u'专利包名称', widget=forms.TextInput(attrs={'class': 'text-input large-input'}))
    desc = forms.CharField(label=u'专利包描述', widget=forms.Textarea(attrs={'class': 'large-input'}))
    rank_catalog_weight = {}

    def __init__(self, *args, **kwargs):
        super(PatentPackageBaseInfoForm, self).__init__(*args, **kwargs)
        self.rank_catalog_weight = {}
        rank_catalog_list = RankCatalog.objects.filter(disabled=False).order_by('sort')
        expert_catalog_list = ExpertCatalog.objects.all()

        for catalog in rank_catalog_list:
            self.fields["rank_%d_weight" % catalog.id] = forms.CharField(
                label=catalog.name,
                widget=forms.NumberInput(attrs={'max': 9, 'min': 1, 'value':2, 'class': 'text-input small-input'}))
            self.rank_catalog_weight["rank_%d_weight" % catalog.id] = self.fields["rank_%d_weight" % catalog.id]

            self.rank_catalog_weight["rank_%d_weight" % catalog.id].expert_weight = {}
            for expert_catalog in expert_catalog_list:
                self.fields["rank_%d_expert_%d_weight" % (catalog.id, expert_catalog.id)] = forms.CharField(
                    label="%s_%s" % (catalog.name, expert_catalog.name),
                    widget=forms.NumberInput(attrs={'max': 9, 'min': 1, 'value':2, 'class': 'text-input small-input'}))

                self.rank_catalog_weight["rank_%d_weight" % catalog.id].expert_weight["rank_%d_expert_%d_weight" % (catalog.id, expert_catalog.id)] = \
                    self.fields["rank_%d_expert_%d_weight" % (catalog.id, expert_catalog.id)]

    def get_expert_catalog(self):
        for catalog in ExpertCatalog.objects.all():
            yield catalog.name

    def get_rank_catalog_weight(self):
        for catalog in self.rank_catalog_weight:
            yield self[catalog], [self[tag] for tag in self.rank_catalog_weight[catalog].expert_weight]


class PatentPackageItemsForm(forms.Form):
    rank_catalog = {}

    def __init__(self, *args, **kwargs):
        super(PatentPackageItemsForm, self).__init__(*args, **kwargs)

        rank_catalog_list = RankCatalog.objects.filter(disabled=False).order_by('sort')
        for catalog in rank_catalog_list:
            items = ((i.id, i.desc) for i in RankItem.objects.filter(catalog=catalog))
            self.fields["catalog_%d_item" % catalog.id] = forms.MultipleChoiceField(label=catalog.name,
                choices=items, widget=forms.CheckboxSelectMultiple())
            self.rank_catalog["catalog_%d_item" % catalog.id] = self.fields["catalog_%d_item" % catalog.id]

    def get_rank_catalog(self):
        for catalog in self.rank_catalog:
            yield self[catalog]

class PatentPackagePatentsForm(forms.Form):
    selected_patent_list = forms.CharField(max_length=4096, label='专利列表', widget=forms.HiddenInput())


class PatentPackageSummaryForm(forms.Form):
    pass

