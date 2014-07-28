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


class PatentRatingListView(ListView):
    model = PatentExpertRating

    def get_context_data(self, **kwargs):
        context = super(PatentRatingListView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['reject_list'] = self.model.objects.filter(expert=self.request.user).exclude(submit_date=None).filter(
            ratings="-1").order_by("report__package")
        context['submit_list'] = self.model.objects.filter(expert=self.request.user).exclude(submit_date=None).exclude(
            ratings="-1").order_by("report__package")
        for o in context['submit_list']:
            ratings = o.ratings.split(',')
            weights = [string.atof(x) / 10 for x in o.report.package.rating_weight.split(',')]
            o.my_rating = 0
            for x in xrange(len(weights)):
                o.my_rating += string.atof(weights[x]) * string.atof(ratings[x])

        return context

    def get_queryset(self):
        object_list = self.model.objects.filter(expert=self.request.user, submit_date=None).exclude(
            report__package__submit_date=None).order_by("report__package")
        # 历史评级 和 用户当前评级
        for o in object_list:
            # 历史评级
            history_report = PatentRatingReport.objects.filter(patent=o.report.patent).exclude(
                finish_date=None).order_by('finish_date')
            if history_report:
                o.current_rating = history_report.first().rank
            else:
                o.current_rating = 0

            # 用户当前评级
            ratings = o.ratings.split(',')
            weights = [string.atof(x) / 10 for x in o.report.package.rating_weight.split(',')]
            o.my_rating = 0
            for x in xrange(len(weights)):
                o.my_rating += string.atof(weights[x]) * string.atof(ratings[x])
        return object_list

