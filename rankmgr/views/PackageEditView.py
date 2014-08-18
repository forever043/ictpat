# -*- coding: UTF-8 -*-
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core import exceptions
from django.core.urlresolvers import reverse_lazy
from django.db import IntegrityError, DatabaseError
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.views.generic import *
from django.views.generic.edit import FormMixin
from libs.django_datatables_view.base_datatable_view import BaseDatatableView
import json

from rankmgr.models import *


class PackageEditView(DetailView):
    model = PatentPackage
    default_referer_url = '/'

    def get_context_data(self, **kwargs):
        context = super(PackageEditView, self).get_context_data(**kwargs)
        context['request'] = self.request
        if '__next__' in self.request.POST:
            context['i__next__'] = self.request.POST['__next__']
        else:
            if 'HTTP_REFERER' in self.request.META:
                context['i__next__'] = self.request.META['HTTP_REFERER']
            else:
                context['i__next__'] = self.default_referer_url
        context['report_list'] = PatentRatingReport.objects.filter(package=self.object)
        for o in context['report_list']:
            o.count = u"%d/3" % PatentExpertRating.objects.filter(report=o).count()
        return context
