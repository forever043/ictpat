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

from rankmgr.models import PatentRatingReport
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

        return context

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
