# -*- coding: UTF-8 -*-
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib import messages

from dashboard.models import ExpertCatalog
from patmgr.models import Patent
from rankmgr.models import *
from rankmgr.forms import PatentPackageBaseInfoForm, PatentPackageItemsForm, PatentPackagePatentsForm, PatentPackageSummaryForm

class PatentPackageWizardView(SessionWizardView):
    model=PatentPackage
    form_list = [ 
        ("base_info", PatentPackageBaseInfoForm),
        ("items",     PatentPackageItemsForm),
        ("patents",   PatentPackagePatentsForm),
        ("summary",   PatentPackageSummaryForm),
    ]
    template_list = { 
        "base_info": "rankmgr/package/0_base_info.html",
        "items":     "rankmgr/package/1_items.html",
        "patents":   "rankmgr/package/2_patents.html",
        "summary":   "rankmgr/package/3_summary.html",
    }

    initial_dict = {
        "matchfield":    { },
    }

    return_url = reverse_lazy('patent-package-list')

    def get_context_data(self, **kwargs):
        context = super(PatentPackageWizardView, self).get_context_data(**kwargs)
        context['request'] = self.request
        if self.steps.current == 'summary':
            cd = self.get_all_cleaned_data()
            summary = {
                'name': cd['name'],
                'desc': cd['desc'],
                'rank_weight': self.__get_rank_weight(cd),
                'item_list': self.__get_item_list(cd),
                'patent_list': Patent.objects.filter(pk__in = 
                    [int(s) for s in cd["selected_patent_list"].split('&') if s!=u""]),
            }
            context.update({'package_summary': summary})

        return context

    def __get_item_list(self, cd):
        catalog_list = []
        rank_catalog_list = RankCatalog.objects.filter(disabled=False).order_by('sort')
        for catalog in rank_catalog_list:
            score = float(cd["rank_%d_weight" % catalog.id])
            items = RankItem.objects.filter(pk__in = [int (s) for s in cd["catalog_%d_item" % catalog.id]])
            total_weight = 0
            for it in items:
                total_weight += int(cd["item_%d_weight" % it.id])
            for it in items:
                it.score = (score *int(cd["item_%d_weight" % it.id]))/total_weight
            catalog_list.append({
                'name': catalog.name,
                'weight': cd["rank_%d_weight" % catalog.id],
                'items': items,
            })
        return catalog_list

    def __get_rank_weight(self, cd):
        rank_weight = []
        rank_catalog_list = RankCatalog.objects.filter(disabled=False).order_by('sort')
        expert_catalog_list = ExpertCatalog.objects.all()
        for catalog in rank_catalog_list:
            expert_weight = []
            # 获取 专家->类别 权重
            for expert_catalog in expert_catalog_list:
                expert_weight.append((expert_catalog.name, cd["rank_%d_expert_%d_weight" % (catalog.id, expert_catalog.id)]))
            # 类别权重+专家类别权重
            rank_weight.append({
                'catalog': catalog.name,
                'weight': cd["rank_%d_weight" % catalog.id],
                'expert_weight': expert_weight,
            })
        return rank_weight

    def get_template_names(self):
        return [self.template_list[self.steps.current]]

    def get_form_initial(self, step):
        return self.initial_dict.get(step, {})

    def done(self, form_list, **kwargs):
        cd = self.get_all_cleaned_data()
        #matchfield_form = form_list[self.get_step_index('matchfield')]
        #import_type = cd['import_type']

        catalog_list = RankCatalog.objects.filter(disabled=False).order_by('sort')
        expert_catalog_list = ExpertCatalog.objects.all()
        patent_list = Patent.objects.filter(pk__in = [int(s) for s in cd["selected_patent_list"].split('&') if s!=u""])

        # 专利包
        package = PatentPackage(name=cd['name'], desc=cd['desc'])
        package.save()
        for catalog in catalog_list:
            # 类别权重
            PatentPackageCatalogWeight(package=package, catalog=catalog,
                                       weight=int(cd["rank_%d_weight" % catalog.id])).save()
            # 专家类别权重
            for expert_catalog in expert_catalog_list:
                ExpertCatalogWeight(package=package,
                                    rank_catalog=catalog, expert_catalog=expert_catalog,
                                    weight=int(cd["rank_%d_expert_%d_weight" % (catalog.id, expert_catalog.id)])).save()
            # 项目列表与权重
            for item in RankItem.objects.filter(pk__in = [int (s) for s in cd["catalog_%d_item" % catalog.id]]):
                PatentPackageRankItem(
                    package=package, item=item,
                    weight=int(cd["item_%d_weight" % item.id])
                ).save()

        # 专利列表
        for patent in patent_list:
            PatentRatingReport(package=package, patent=patent).save()
  
        #if success_count > 0:
        messages.success(self.request, u'专利包"%s"创建成功' % cd["name"])
        #if error_count > 0:
        #    messages.error(self.request, u"专利包创建失败")

        return HttpResponseRedirect(self.return_url)

