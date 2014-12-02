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

from django.contrib.auth.models import User
from rankmgr.models import *

class ExpertListJson(BaseDatatableView):
    model = User
    columns = []
    column_template = {}

    def __init__(self, *args, **kwargs):
        super(ExpertListJson, self).__init__(*args, **kwargs)
        if 'pk' not in self.columns:
            self.columns.append('pk')
            self.columns.append('DT_RowId')

    def get_initial_queryset(self):
        if not self.model:
            raise NotImplementedError("Need to provide a model or implement get_initial_queryset!")
        return self.model.objects.filter(groups__name=u'评审专家')

    def render_column(self, row, column):
        if column in self.column_template:
            return self.column_template[column](row)
        elif column == 'DT_RowId':
            return '%d' % (row.pk)
        return super(ExpertListJson, self).render_column(row, column)

