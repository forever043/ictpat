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

from scrmgr.models import *
from scrmgr.forms import *

class SCRFreshListView(RedirectView):
	def get(self, request, *args, **kwargs):
		request.session['scr-filter'] = {}
		return super(SoftwareFreshListView, self).get(request, *args, **kwargs)

class SCRListView(ListView, FormMixin):
	model = Software
	form_class = SoftwareFilterForm
	context_object_name = 'scr_list'
	template_name = 'scrmgr/list_scr.html'
	paginate_by = 10
	success_url = reverse_lazy('scr-list')

	def get_context_data(self, **kwargs):
		context = super(SoftwareListView, self).get_context_data(**kwargs)
		context['request'] = self.request
		context['form'] = self.form
		return context

	def get(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		self.form = self.get_form(form_class)
		return super(SoftwareListView, self).get(request, *args, **kwargs)

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
		scr_filter_list = self.request.session.get('scr-filter', {})
		for (filter_name, filter_value) in scr_filter_list.items():
			if 'pk' in filter_value:
				initial[filter_name] = filter_value['pk']
			elif 'str' in filter_value:
				initial[filter_name] = filter_value['str']
		return initial

	def get_queryset(self):
		scr_filter_list = self.request.session.get('scr-filter', {})
		messages.warning(self.request, scr_filter_list)
		object_filter = {}
		for (filter_name, filter_value) in scr_filter_list.items():
                        if 'pk' in filter_value:
                                object_filter[filter_name] = filter_value['pk']
                        elif 'str' in filter_value:
                                object_filter[filter_name + '__icontains'] = filter_value['str']
		object_list = self.model.objects.filter(**object_filter)
		if not object_list:
			messages.warning(self.request, "没有找到符合条件的软件")

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
		self.request.session['scr-filter'] = filter
		return super(SoftwareListView, self).form_valid(form)

	def form_invalid(self, form):
		return super(SoftwareListView, self).form_invalid(form)


class SCRDetailView(DetailView):
	model = Software
	context_object_name = 'scr'
	template_name = 'scrmgr/scr_detail.html'
	
	def get_context_data(self, **kwargs):
		context = super(SoftwareDetailView, self).get_context_data(**kwargs)
		context['request'] = self.request
		if '__next__' in self.request.POST:
			context['i__next__'] = self.request.POST['__next__']
		else:
			if 'HTTP_REFERER' in self.request.META:
				context['i__next__'] = self.request.META['HTTP_REFERER']
			else:
				context['i__next__'] = reverse_lazy('scr-list')
		return context


class SCRCreateView(SuccessMessageMixin, CreateView):
	model = Software
	form_class = SoftwareExtForm
	template_name = 'scrmgr/add_scr_basic.html'
	success_url = reverse_lazy('scr-add')
	success_message = u'软件 "%(name)s" 添加成功'

	def get_context_data(self, **kwargs):
		context = super(SoftwareCreateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_invalid(self, form):
		error_msg = u'信息更新失败'
		messages.error(self.request, error_msg)
		return super(SoftwareCreateView, self).form_invalid(form)


class SCRBatchAddView(FormView):
	template_name = 'scrmgr/add_scr_batch.html'
	form_class = SoftwareBatchAddForm
	success_url = reverse_lazy('scr-batchadd')

	def get_context_data(self, **kwargs):
		context = super(SoftwareBatchAddView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def get_success_message(self, cleaned_data):
		messages.error(self.request, cleaned_data['content'])
		return u'软件添加成功' + cleaned_data['content']

	def form_valid(self, form):
		batch_message = ''
		has_error = False
		content = form.cleaned_data['content']
		for line in content.split('\n'):
			scrdata = line.strip().split('\t')
			scr = Software(name = patdata[1],
					department = Department.objects.get(name=patdata[0]),
					inventors = patdata[2],
					type = SoftwareType.objects.get(name='发明软件'),
					state = SoftwareState.objects.get(name='审核中'),
					apply_code = patdata[3],
					apply_date = patdata[4])

			error_msg = ''
			try:
				scr.save();
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

		return super(SoftwareBatchAddView, self).form_valid(form)
	
	def form_invalid(self, form):
		error_msg = u'批量添加失败'
		messages.error(self.request, error_msg)
		return super(SoftwareBatchAddView, self).form_invalid(form)


class SCRUpdateView(SuccessMessageMixin, UpdateView):
	model = Software
	form_class = SoftwareExtForm
	template_name = 'scrmgr/edit_scr.html'
	success_message = u'软件 "%(name)s" 信息更新成功'
	error_message = u'软件 "%(name)s" 信息更新失败'

	def get_context_data(self, **kwargs):
		context = super(SoftwareUpdateView, self).get_context_data(**kwargs)
		context['request'] = self.request

		if '__next__' in self.request.POST:
			context['i__next__'] = self.request.POST['__next__']
		else:
			if 'HTTP_REFERER' in self.request.META:
				context['i__next__'] = self.request.META['HTTP_REFERER']
			else:
				context['i__next__'] = reverse_lazy('scr-list')

		return context

	def get_success_message(self, cleaned_data):
		return self.success_message % cleaned_data

	def get_success_url(self):
		return self.request.POST['__next__']

	def get_initial(self):
		initial = {}
		extfields_list = SoftwareExtField.objects.filter(scr=self.object)
		for extfield in extfields_list:
			initial[extfield.type.field_name] = extfield.value
		return initial

	def form_invalid(self, form):
		messages.error(self.request, self.error_message % dict(name=self.object.name))
		return super(SoftwareUpdateView, self).form_invalid(form)


class SCRDeleteView(DeleteView):
	model = Software
	success_url = reverse_lazy('scr-list')

	# allow delete only logged in user by appling decorator
	#@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		# maybe do some checks here for permissions ...
		resp = super(SoftwareDeleteView, self).dispatch(*args, **kwargs)
		if self.request.is_ajax():
			response_data = {"result": "ok"}
			return HttpResponse(json.dumps(response_data),
				content_type="application/json")
		else:
			return resp

