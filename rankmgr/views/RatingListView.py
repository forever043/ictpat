# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import *
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.core import exceptions
import json
import string

from rankmgr.models import *
import RatingScore


class PatentRatingListView(ListView):
    model = PatentExpertRating

    def get_context_data(self, **kwargs):
        context = super(PatentRatingListView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['reject_list'] = self.model.objects.filter(expert=self.request.user).exclude(submit_date=None).filter(
            ratings="-1").order_by("report__package")
        context['submit_list'] = self.model.objects.filter(expert=self.request.user).exclude(submit_date=None).exclude(
            ratings="-1").order_by("report__package").order_by("submit_date")
        for o in context['submit_list']:
            o.my_rating = RatingScore.get_package_rating_score(o)

        return context

    def get_queryset(self):
        object_list = self.model.objects.filter(expert=self.request.user, submit_date=None).exclude(
            report__package__submit_date=None).order_by("report__package")
        # 评分完成度 + 我的评分
        for o in object_list:
            # 评分完成度
            o.total_items = len(RatingScore.get_package_rank_item(o.report.package))
            o.finished_items = len(RatingScore.get_rating_finished(o))

            # 用户当前评级
            o.my_rating = RatingScore.get_package_rating_score(o)

        return object_list

