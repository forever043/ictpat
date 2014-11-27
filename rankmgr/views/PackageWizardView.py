# -*- coding: UTF-8 -*-
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib import messages

from rankmgr.models import PatentPackage
from rankmgr.forms import PatentPackageBaseInfoForm, PatentPackageItemsForm, PatentPackagePatentsForm

class PatentPackageWizardView(SessionWizardView):
    model=PatentPackage
    form_list = [ 
        ("base_info", PatentPackageBaseInfoForm),
        ("items",     PatentPackageItemsForm),
        ("patents",   PatentPackagePatentsForm),
    ]
    template_list = { 
        "base_info": "rankmgr/package/0_base_info.html",
        "items":     "rankmgr/package/1_items.html",
        "patents":   "rankmgr/package/2_patents.html",
    }

    initial_dict = {
        "matchfield":    {
                "department": "0",
                "name":    "1",
                "inventors": "2",
                "apply_code": "3",
                "apply_date": "4",
                "state": "5",
                "authorize_code": "6",
                "authorize_date": "7",
                "type": "9",
        },
    }
    return_url = reverse_lazy('patent-package-list')

    def get_context_data(self, **kwargs):
        context = super(PatentPackageWizardView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context

    def get_template_names(self):
        return [self.template_list[self.steps.current]]

    def get_form_initial(self, step):
        return self.initial_dict.get(step, {})

    def done(self, form_list, **kwargs):
        cd = self.get_all_cleaned_data()
        #matchfield_form = form_list[self.get_step_index('matchfield')]
        #import_type = cd['import_type']

        #if success_count > 0:
        messages.success(self.request, u"专利包创建成功")
        #if error_count > 0:
        #    messages.error(self.request, u"专利包创建失败")

        return HttpResponseRedirect(self.return_url)

