from django.shortcuts import render
from django.views.generic import ListView

from patmgr.models import *

# Create your views here.
class MetaMgrView(ListView):
	template_name = 'sysmgr/metamgr.html'
	context_object_name = 'department_list'	
	queryset = Department.objects.all().order_by('name')

	def get_context_data(self, **kwargs):
		context = super(MetaMgrView, self).get_context_data(**kwargs)
		context['patent_extfield_type_list'] = PatentExtFieldType.objects.all()
		context['patent_state_list'] = PatentState.objects.all()
		context['patent_type_list'] = PatentType.objects.all()
		return context

