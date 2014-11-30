# coding=utf-8
from django import forms
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from dashboard.models import ExpertCatalog
from rankmgr.models import RankCatalog, RankItem

class PatentPackageBaseInfoForm(forms.Form):
    name = forms.CharField(label=u'专利包名称', widget=forms.TextInput(attrs={'class': 'text-input large-input'}))
    desc = forms.CharField(label=u'专利包描述', required=False, widget=forms.Textarea(attrs={'class': 'large-input'}))
    rank_catalog_weight = []

    def __init__(self, *args, **kwargs):
        super(PatentPackageBaseInfoForm, self).__init__(*args, **kwargs)
        self.rank_catalog_weight = []
        rank_catalog_list = RankCatalog.objects.filter(disabled=False).order_by('sort')
        expert_catalog_list = ExpertCatalog.objects.all()

        for catalog in rank_catalog_list:
            self.fields["rank_%d_weight" % catalog.id] = forms.CharField(
                label=catalog.name,
                widget=forms.NumberInput(attrs={'max': 100, 'min': 10, 'value':10, 'step': 10, 'class': 'text-input small-input'}))

            expert_weight = []
            for expert_catalog in expert_catalog_list:
                self.fields["rank_%d_expert_%d_weight" % (catalog.id, expert_catalog.id)] = forms.CharField(
                    label="%s_%s" % (catalog.name, expert_catalog.name),
                    widget=forms.NumberInput(attrs={'max': 9, 'min': 1, 'value':2, 'class': 'text-input small-input'}))
                expert_weight.append({
                    'name': "rank_%d_expert_%d_weight" % (catalog.id, expert_catalog.id),
                    'weight': self.fields["rank_%d_expert_%d_weight" % (catalog.id, expert_catalog.id)]
                })

            self.rank_catalog_weight.append({
                'name': "rank_%d_weight" % catalog.id,
                'weight': self.fields["rank_%d_weight" % catalog.id],
                'expert_weight': expert_weight,
            })

    def get_expert_catalog(self):
        for catalog in ExpertCatalog.objects.all():
            yield catalog.name

    def get_rank_catalog_weight(self):
        for catalog in self.rank_catalog_weight:
            yield self[catalog["name"]], [self[expert["name"]] for expert in catalog["expert_weight"]]


class PatentPackageItemsForm(forms.Form):
    rank_catalog = {}
    item_weight = []

    def __init__(self, *args, **kwargs):
        super(PatentPackageItemsForm, self).__init__(*args, **kwargs)

        self.rank_catalog = {}
        self.item_weight = []

        rank_catalog_list = RankCatalog.objects.filter(disabled=False).order_by('sort')
        for catalog in rank_catalog_list:
            items = ((i.id, i.desc) for i in RankItem.objects.filter(catalog=catalog))
            self.fields["catalog_%d_item" % catalog.id] = forms.MultipleChoiceField(label=catalog.name,
                choices=items, widget=forms.CheckboxSelectMultiple())
            self.rank_catalog["catalog_%d_item" % catalog.id] = self.fields["catalog_%d_item" % catalog.id]
			# 问题权重输入框
            for item in RankItem.objects.filter(catalog=catalog):
                self.fields["item_%d_weight" % item.id] = forms.CharField(label=u"%s"%item.desc,
                    widget=forms.NumberInput(attrs={'max': 10, 'min': 1, 'value':1, 'class': 'text-input small-input'})) 
                self.item_weight.append("item_%d_weight" % item.id)

    def get_rank_catalog(self):
        for catalog in self.rank_catalog:
            yield self[catalog]

    def get_item_weight(self):
		for item in self.item_weight:
			yield self[item]

class PatentPackagePatentsForm(forms.Form):
    selected_patent_list = forms.CharField(max_length=4096, label='专利列表', widget=forms.HiddenInput())


class PatentPackageSummaryForm(forms.Form):
    pass

