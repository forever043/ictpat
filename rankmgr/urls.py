# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required

from dashboard.views import *
from patmgr.models import *
from rankmgr.models import *
from rankmgr.views import *
from rankmgr.forms import *

urlpatterns = patterns('',
    url(r'^$', login_required(RedirectView.as_view(pattern_name='patent-list')), name='rank'),
    url(r'^summary/$', login_required(RankSummaryView.as_view()), name='rank-summary'),
    url(r'^expert/$', login_required(RankExpertListView.as_view()), name='rank-expert-list'),

	# Patent Rating Manager
	## 专利包列表
	url(r'^package/$',
		login_required(PatentPackageListView.as_view(
			context_object_name = 'package_list',
			template_name='rankmgr/patent_package_list.html')),
		name='patent-package-list'),

	## 专利包创建
	url(r'^package/add/$',
		login_required(DashMgrCreateView.as_view(
				model = PatentPackage,
				form_class = PatentPackageCreateForm,
				template_name='rankmgr/patent_package_add.html',
				success_url = reverse_lazy('patent-package-list'),
				success_message = u'专利包 "%(name)s" 添加成功',
				error_message = u'专利包失败')),
		name='patent-package-add'),

	## 专利包提交
	url(r'^package/(?P<pk>\d+)/edit/$',
		login_required(DashMgrDetailView.as_view(
				model = PatentPackage,
				context_object_name = 'patpkg',
				template_name='rankmgr/patent_package_edit.html',
				default_referer_url = reverse_lazy('patent-package-list'))),
		name='patent-package-edit'),
	url(r'package/(?P<pk>\d+)/submit/$',	# 提交一个专利包
		login_required(DashMgrRatingPackageSubmit.as_view(
			return_url = reverse_lazy('patent-package-list'))),
		name='patent-package-submit'),
	url(r'^package/(?P<pk>\d+)/data/patent/$',
		login_required(DashMgrListJson.as_view(
			model = PatentRatingReport,
			initial_list = ["package"],
			columns = [ 'name', 'department', 'count' ],
			column_template = { 
				"name":			lambda o: o.patent.name,
				"department":	lambda o: o.patent.department.name,
				"count":		lambda o: u"%d/3" % PatentExpertRating.objects.filter(patent=o).count() })),
		name='patent-package-edit-json'),

	url(r'package/(?P<pk>\d+)/experts/$',			# 获取某一专利的评审专家列表
		login_required(DashMgrListJson.as_view(
			model = PatentExpertRating, initial_list = ["patent"],
			columns = [ 'expert' ],
			column_template = { "expert":	lambda o: o.expert.pk})),
		name='patent-package-patent-experts-json'),
	url(r'package/(?P<pk>\d+)/experts/add/$',			# 增加某一专利的评审专家列表 ?patent=%d&expert=%d
		login_required(DashMgrRatingExpertAdd.as_view(
			model = PatentExpertRating)),
		name='patent-package-patent-experts-add'),
	url(r'package/(?P<pk>\d+)/experts/del/$',			# 删除某一专利的评审专家列表 ?patent=%d&expert=%d
		login_required(DashMgrRatingExpertDel.as_view(
			model = PatentExpertRating)),
		name='patent-package-patent-experts-del'),
		

	## 专利包查看
	url(r'^package/(?P<pk>\d+)/$',
		login_required(DashMgrDetailView.as_view(
				model = PatentPackage,
				context_object_name = 'patpkg',
				template_name='rankmgr/patent_package_detail.html',
				default_referer_url = reverse_lazy('patent-package-list'))),
		name='patent-package-detail'),
	url(r'^package/(?P<pk>\d+)/data/$',
		login_required(DashMgrListJson.as_view(
			model = PatentExpertRating,
			#retrieve_list = ["package"],
			initial_list = ["package"],
			initial_order = ["patent"],
			columns = [ 'patent', 'expert', 'rank', 'remark', 'state', 'submit_date' ],
			column_template = { 
				"patent": lambda o: u'&nbsp;(%d/%d)&nbsp;&nbsp;%s<span style="float:right;"><a href="#">撰写评级报告</a></span>' % (
											PatentExpertRating.objects.filter(patent=o.patent).filter(submit_date__gt="1900-01-01").count(),
											PatentExpertRating.objects.filter(patent=o.patent).count(),
											o.patent.patent.name),
				"expert": lambda o: u'%s' % o.expert.last_name + o.expert.first_name,
				"rank":   lambda o: u'%s' % o.rank if o.rank else "----",
				"remark": lambda o: u'%s' % o.remark if o.remark else "----",
				"state":  lambda o: u'%s' % u'已完成' if o.submit_date else u'进行中',
				"submit_date": lambda o: u'%s' % o.submit_date if o.remark else "----",
				"pk":	  lambda o: u'<a href="%(url)s" title="更换专家"><img src="/resources/images/icons/hammer_screwdriver.png" alt="更换专家" />更换专家</a>'
									  % { "url":  reverse_lazy('patent-package-detail', args=[o.pk]) } if not o.submit_date else u'' })), 
		name='patent-package-detail-json'),

	########## 专家评价界面 ########
	# 待评专利列表
	url(r'^rating/list/$',
		login_required(PatentRatingListView.as_view(
			context_object_name = 'rating_list',
			template_name = 'rankmgr/patent_rating_list.html')),
			name='patent-rating-list'),
	url(r'^rating/(?P<pk>\d+)/$',
		login_required(PatentRatingDetailView.as_view(
				model = PatentExpertRating,
				form_class = PatentExpertRatingForm,
				template_name = 'rankmgr/patent_rating_detail.html',
				default_referer_url = reverse_lazy('patent-rating-list'),
				success_message = u'专利 "%(name)s" 评价成功',
				error_message = u'专利 "%(name)s" 评价失败')),
		name='patent-rating-detail'),
)

