# coding=utf-8
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import *
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from django.core import exceptions
import json

from patmgr.models import *
from patmgr.forms import *

class PatentFreshListView(RedirectView):
	def get(self, request, *args, **kwargs):
		request.session['patent-filter'] = {}
		return super(PatentFreshListView, self).get(request, *args, **kwargs)

class PatentListView(ListView, FormMixin):
	model = Patent
	form_class = PatentFilterForm
	context_object_name = 'patent_list'
	template_name = 'patmgr/list_patent.html'
	paginate_by = 10
	success_url = reverse_lazy('patent-list')

	def get_context_data(self, **kwargs):
		context = super(PatentListView, self).get_context_data(**kwargs)
		context['request'] = self.request
		context['form'] = self.form
		return context

	def get(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		self.form = self.get_form(form_class)
		return super(PatentListView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid():
			self.form_valid(form)
		else:
			self.form_invalid(form)  
		return self.get(request, *args, **kwargs)

	def get_initial(self):
		initial = {}
		patent_filter_list = self.request.session.get('patent-filter', {})
		for (filter_name, filter_value) in patent_filter_list.items():
			if 'pk' in filter_value:
				initial[filter_name] = filter_value['pk']
			elif 'str' in filter_value:
				initial[filter_name] = filter_value['str']
		return initial

	def get_queryset(self):
		patent_filter_list = self.request.session.get('patent-filter', {})
		messages.warning(self.request, patent_filter_list)
		object_filter = {}
		for (filter_name, filter_value) in patent_filter_list.items():
                        if 'pk' in filter_value:
                                object_filter[filter_name] = filter_value['pk']
                        elif 'str' in filter_value:
                                object_filter[filter_name + '__icontains'] = filter_value['str']
		object_list = self.model.objects.filter(**object_filter)
		if not object_list:
			messages.warning(self.request, "没有找到符合条件的专利")

		return object_list

	def form_valid(self, form):
		filter = {}
		for (field, value) in form.cleaned_data.items():
			if value:
				if isinstance(value, models.Model):
					filter[field] = {'pk': value.pk}
				else:
					#filter[field+'__icontains'] = value
					filter[field] = {'str': value}
		self.request.session['patent-filter'] = filter
		return super(PatentListView, self).form_valid(form)

	def form_invalid(self, form):
		return super(PatentListView, self).form_invalid(form)


class PatentDetailView(DetailView):
	model = Patent
	context_object_name = 'patent'
	template_name = 'patmgr/patent_detail.html'
	
	def get_context_data(self, **kwargs):
		context = super(PatentDetailView, self).get_context_data(**kwargs)
		context['request'] = self.request
		if '__next__' in self.request.POST:
			context['i__next__'] = self.request.POST['__next__']
		else:
			if 'HTTP_REFERER' in self.request.META:
				context['i__next__'] = self.request.META['HTTP_REFERER']
			else:
				context['i__next__'] = reverse_lazy('patent-list')
		return context


class PatentCreateView(SuccessMessageMixin, CreateView):
	model = Patent
	form_class = PatentExtForm
	template_name = 'patmgr/add_patent_basic.html'
	success_url = reverse_lazy('patent-add')
	success_message = u'专利 "%(name)s" 添加成功'

	def get_context_data(self, **kwargs):
		context = super(PatentCreateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_invalid(self, form):
		error_msg = u'信息更新失败'
		messages.error(self.request, error_msg)
		return super(PatentCreateView, self).form_invalid(form)


class PatentBatchAddView(FormView):
	template_name = 'patmgr/add_patent_batch.html'
	form_class = PatentBatchAddForm
	success_url = reverse_lazy('patent-batchadd')

	def get_context_data(self, **kwargs):
		context = super(PatentBatchAddView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def get_success_message(self, cleaned_data):
		messages.error(self.request, cleaned_data['content'])
		return u'专利添加成功' + cleaned_data['content']

	def form_valid(self, form):
		batch_message = ''
		has_error = False
		content = form.cleaned_data['content']
		for line in content.split('\n'):
			patdata = line.strip().split('\t')
			patent = Patent(name = patdata[1],
					department = Department.objects.get(name=patdata[0]),
					inventors = patdata[2],
					type = PatentType.objects.get(name='发明专利'),
					state = PatentState.objects.get(name='审核中'),
					apply_code = patdata[3],
					apply_date = patdata[4])

			error_msg = ''
			try:
				patent.save();
			except IntegrityError, x:
				error_msg = u"数据约束错误: " + x.__unicode__()
			except DatabaseError, x:
				error_msg = u"数据库错误: " + x.__unicode__()
			except:
				error_msg = u"未知错误"
			if not error_msg:
				batch_message += u'"' + patdata[1] + u'"添加成功\n'
			else:
				batch_message += u'"' + patdata[1] + u'"添加失败：' + error_msg + '\n'
				has_error = True

		if has_error:
			messages.warning(self.request, batch_message)
		else:
			messages.success(self.request, batch_message)

		return super(PatentBatchAddView, self).form_valid(form)
	
	def form_invalid(self, form):
		error_msg = u'批量添加失败'
		messages.error(self.request, error_msg)
		return super(PatentBatchAddView, self).form_invalid(form)


class PatentUpdateView(SuccessMessageMixin, UpdateView):
	model = Patent
	form_class = PatentExtForm
	template_name = 'patmgr/edit_patent.html'
	success_message = u'专利 "%(name)s" 信息更新成功'
	error_message = u'专利 "%(name)s" 信息更新失败'

	def get_context_data(self, **kwargs):
		context = super(PatentUpdateView, self).get_context_data(**kwargs)
		context['request'] = self.request

		if '__next__' in self.request.POST:
			context['i__next__'] = self.request.POST['__next__']
		else:
			if 'HTTP_REFERER' in self.request.META:
				context['i__next__'] = self.request.META['HTTP_REFERER']
			else:
				context['i__next__'] = reverse_lazy('patent-list')

		return context

	def get_success_message(self, cleaned_data):
		return self.success_message % cleaned_data

	def get_success_url(self):
		return self.request.POST['__next__']

	def get_initial(self):
		initial = {}
		extfields_list = PatentExtField.objects.filter(patent=self.object)
		for extfield in extfields_list:
			initial[extfield.type.field_name] = extfield.value
		return initial

	def form_invalid(self, form):
		messages.error(self.request, self.error_message % dict(name=self.object.name))
		return super(PatentUpdateView, self).form_invalid(form)

	# Comment out for "Save/SaveAndReturn"
	#def form_valid(self, form):
	#	# save_and_return click
	#	if self.request.POST.get('save_and_return', None):
	#		self.success_url = self.request.POST['__next__']
	#	else:
	#		self.success_url = reverse_lazy('patent-edit', args=(self.object.pk,))
	#	return super(PatentUpdateView, self).form_valid(form)
	

#class PatentEditView(SuccessMessageMixin, FormView):
#	form_class = PatentEditForm
#	template_name = 'patmgr/edit_patent.html'
#	success_message = u'专利 "%(name)s" 信息更新成功'
#	error_message = u'专利 "%(name)s" 信息更新失败'
#
#	def get_context_data(self, **kwargs):
#		context = super(PatentEditView, self).get_context_data(**kwargs)
#		context['request'] = self.request
#		return context
#
#	def get_success_message(self, cleaned_data):
#		return self.success_message % cleaned_data['basic']
#
#	def form_valid(self, form):
#		basic_cd = form.cleaned_data['basic']
#		extent_cd = form.cleaned_data['extent']
#		return super(PatentEditView, self).form_valid(form)
#
#	def form_invalid(self, form):
#		messages.error(self.request, self.error_message % dict(name=self.object.name))
#		return super(PatentEditView, self).form_invalid(form)


class PatentDeleteView(DeleteView):
	model = Patent
	success_url = reverse_lazy('patent-list')

	# allow delete only logged in user by appling decorator
	#@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		# maybe do some checks here for permissions ...
		resp = super(PatentDeleteView, self).dispatch(*args, **kwargs)
		if self.request.is_ajax():
			response_data = {"result": "ok"}
			return HttpResponse(json.dumps(response_data),
				content_type="application/json")
		else:
			return resp


class PatentRetrieveManager(FormView):
	template_name = 'patmgr/patlist.html'
	form_class = PatentRetrieveConfigForm
	success_url = reverse_lazy('patent-retvmgr')

	def get_context_data(self, **kwargs):
		context = super(PatentRetrieveManager, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def get_success_message(self, cleaned_data):
		return u'保存成功'

	def form_valid(self, form):
		return super(PatentRetrieveManager, self).form_valid(form)
