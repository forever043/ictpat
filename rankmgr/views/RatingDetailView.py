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


class PatentRatingDetailView(SuccessMessageMixin, UpdateView):
    error_message = u'"%(name)s" 评价失败'
    default_referer_url = '/'

    def get_context_data(self, **kwargs):
        context = super(PatentRatingDetailView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['patent'] = self.object.report.patent
        context['ratings'] = self.object.ratings.split(',')
        context['weights'] = [string.atof(x)/10 for x in self.object.report.package.rating_weight.split(',')]
        context['history_rating'] = self.model.objects.filter(report__patent=self.object.report.patent).exclude(report=self.object.report).exclude(submit_date=None).exclude(ratings=-1).order_by("submit_date")

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
