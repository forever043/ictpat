# coding=utf-8
from django import forms
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from  patmgr.models import Patent
from rankmgr.models import *
from rankmgr.views import RatingScore

class PatentRatingPageForm(forms.ModelForm):
    action = forms.CharField(widget=forms.HiddenInput(), initial="save")
    rank_catalog = []

    class Meta:
        model = PatentExpertRating
        fields = [ 'ratings', 'remark', 'submit_date' ]
        widgets = {
            'ratings':   forms.HiddenInput(),
            'remark': forms.Textarea(attrs={'class':'text-input large-input'}),
        }
    def __init__(self, *args, **kwargs):
        super(PatentRatingPageForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.submit_date:
            self.fields['ratings'].widget.attrs['disabled'] = 'disabled'
            self.fields['remark'].widget.attrs['readonly'] = True

        self.rank_catalog = []
        for catalog in RankCatalog.objects.filter(disabled=False).order_by('sort'):
            items = []
            for rank_item in PatentPackageRankItem.objects.filter(package=instance.report.package, item__catalog=catalog):
                options = []
                optIdx = ['optA', 'optB', 'optC', 'optD', 'optE', 'optF']
                for opt in range(0, rank_item.item.optNr):
                    options.append((opt, getattr(rank_item.item, optIdx[opt], '')))
                self.fields["item_%d" % rank_item.item.id] = forms.ChoiceField(label=rank_item.item.desc, choices=options,
                    widget=forms.RadioSelect, required=False)
                items.append("item_%d" % rank_item.item.id)
            self.rank_catalog.append((catalog.name, items))

    def get_rank_catalog(self):
        for name, item_list in self.rank_catalog:
            yield (name, [self[item] for item in item_list])

    def save(self, commit=True):
        if self.cleaned_data["action"] == "submit":
            self.instance.submit_date = datetime.now()
        elif self.cleaned_data["action"] == "reject":
            self.instance.submit_date = datetime.now()
            self.instance.ratings = "-1"
        else:
            self.instance.submit_date = None
        instance = super(PatentRatingPageForm, self).save(commit)

        option_idx = { opt.index: opt for opt in RankOption.objects.all() }

        for item in [rank.item for rank in PatentPackageRankItem.objects.filter(package=instance.report.package)]:
            try:
                sel = RatingSelect.objects.get(rating=instance, item=item)
            except ObjectDoesNotExist:
                sel = RatingSelect(rating=instance, item=item)
            opt = self.cleaned_data['item_%d' % item.id]
            if not opt == '':
                sel.select = option_idx[int(opt)]
                sel.save()

        # 如果总评分可用，更新到数据库
        score = RatingScore.get_package_rating_score(instance)
        if not score == -1:
            instance.ratings = score
            instance.save()

        return instance

