# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import *
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.core import exceptions
import json
import string

from rankmgr.models import *
from retrvhome.views import FileServeView


class PatentRatingDetailView(SuccessMessageMixin, UpdateView):
    error_message = u'"%(name)s" 评价失败'
    default_referer_url = '/'

    def get_context_data(self, **kwargs):
        context = super(PatentRatingDetailView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['patent'] = self.object.report.patent
        context['ratings'] = self.object.ratings.split(',')
        context['weights'] = [string.atof(x)/10 for x in self.object.report.package.rating_weight.split(',')]
        context['history_rating'] = PatentRatingReport.objects.filter(patent=self.object.report.patent)\
                                                              .exclude(package=self.object.report.package)\
                                                              .exclude(finish_date=None)
        # 判断文件是否存在
        context['rankfile_exist'] = FileServeView().exist('rankfile', self.object.report.patent.apply_code)
        context['specfile_exist'] = FileServeView().exist('specfile', self.object.report.patent.apply_code)

        # 查询上一条和下一条记录
        if self.object.submit_date:
            context['state'] = 'submit'
            prev_rank_list = self.model.objects.filter(expert=self.request.user)   \
                                        .exclude(submit_date=None)                 \
                                        .exclude(report__package__submit_date=None)\
                                        .filter(pk__lt=self.object.pk)             \
                                        .order_by("report__package").order_by("submit_date")
            next_rank_list = self.model.objects.filter(expert=self.request.user)   \
                                        .exclude(submit_date=None)                 \
                                        .exclude(report__package__submit_date=None)\
                                        .filter(pk__gt=self.object.pk)             \
                                        .order_by("report__package").order_by("submit_date")
        else:
            context['state'] = 'pending'
            prev_rank_list = self.model.objects.filter(expert=self.request.user)   \
                                        .filter(submit_date=None)                  \
                                        .exclude(report__package__submit_date=None)\
                                        .filter(pk__lt=self.object.pk)             \
                                        .order_by("report__package")
            next_rank_list = self.model.objects.filter(expert=self.request.user)   \
                                        .filter(submit_date=None)                  \
                                        .exclude(report__package__submit_date=None)\
                                        .filter(pk__gt=self.object.pk)             \
                                        .order_by("report__package")
 
        if prev_rank_list:
            context['rating_prev'] = prev_rank_list[len(prev_rank_list)-1].pk
        if next_rank_list:
            context['rating_next'] = next_rank_list[0].pk

        if not self.object.submit_date:
            context['i__next__'] = reverse_lazy('patent-rating-list')
        else:
            context['i__next__'] = reverse_lazy('submit-patent-rating-list')

        # 评分统计表格
        summary = []
        overall_score = 0
        for catalog in RankCatalog.objects.filter(disabled=False).order_by('sort'):
            score = PatentPackageCatalogWeight.objects.get(package=self.object.report.package, catalog=catalog).weight
            count = len(PatentPackageRankItem.objects.filter(package=self.object.report.package, item__catalog=catalog))
            finish_count = len(RatingSelect.objects.filter(rating=self.object, item__catalog=catalog))
            if count == finish_count:
                item_list = PatentPackageRankItem.objects.filter(package=self.object.report.package, item__catalog=catalog)
                total_weight = 0
                for item in item_list:
                    total_weight += item.weight
                final_score = 0
                for item in item_list:
                    item_score = float(score * item.weight)/total_weight
                    select_percent = float(item.item.optNr - RatingSelect.objects.get(rating=self.object, item=item.item).select.index)/item.item.optNr
                    final_score += item_score * select_percent

                if overall_score >= 0:
                    overall_score+=final_score
            else:
                final_score = '----'
                overall_score = -1
            summary.append({
                'name': catalog.name,
                'score': score,
                'count': count,
                'finish_count': finish_count,
                'final_score': final_score,
            })
        context['summary'] = summary
        context['overall_score'] = overall_score if overall_score >= 0 else '----'

        return context

    def get_initial(self):
        initial = {}
        for rating in RatingSelect.objects.filter(rating__report=self.object.report):
            initial.update({'item_%d' % rating.item.id: rating.select.index})
        return initial 

    def get_success_message(self, cleaned_data):
        if self.request.POST["action"] == "save":
            return u'专利"%(name)s"评价草稿保存成功' % { 'name': self.object.report.patent.name }
        return self.success_message % dict(cleaned_data, **{'name':self.object.report.patent.name})

    def get_success_url(self):
        if self.request.POST["action"] == "save":
            return ""
        return self.request.POST['__next__']

    def form_invalid(self, form):
        error_msg = u'信息更新失败'
        messages.error(self.request, error_msg)
        return super(PatentRatingDetailView, self).form_invalid(form)
