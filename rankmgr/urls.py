# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required

from dashboard.views import *
from dashboard.forms import ExpertProfileForm, ExpertProfileEditForm
from patmgr.models import *
from rankmgr.models import *
from rankmgr.views import *
from rankmgr.forms import *


urlpatterns = patterns('',
                       url(r'^$', login_required(RedirectView.as_view(pattern_name='patent-list')), name='rank'),
                       url(r'^summary/$', login_required(RankSummaryView.as_view()), name='rank-summary'),

                       # 专家用户管理
                       url(r'^expert/$',
                           login_required(RankExpertListView.as_view(
                               context_object_name='expert_list')),
                           name='rank-expert-list'),
                       url(r'^expert/add/$',
                           login_required(CreateView.as_view(
                               template_name='rankmgr/expert_add.html',
                               model=User,
                               form_class=ExpertProfileForm,
                               success_url=reverse_lazy('rank-expert-list'))),
                           name='rank-expert-add'),
                       url(r'^expert/(?P<pk>\d+)/edit/$',
                           login_required(UpdateView.as_view(
                               template_name='rankmgr/expert_edit.html',
                               model=User,
                               form_class=ExpertProfileEditForm,
                               success_url=reverse_lazy('rank-expert-list'))),
                           name='rank-expert-edit'),  # Patent Rating Manager  # # 专利包列表
                       url(r'^package/$',
                           login_required(PatentPackageListView.as_view(
                               context_object_name='package_list',
                               template_name='rankmgr/patent_package_list.html')),
                           name='patent-package-list'),  ## 专利包创建
                       url(r'^package/add/$',
                           login_required(DashMgrCreateView.as_view(
                               model=PatentPackage,
                               form_class=PatentPackageCreateForm,
                               template_name='rankmgr/patent_package_add.html',
                               success_url=reverse_lazy('patent-package-list'),
                               success_message=u'专利包 "%(name)s" 添加成功',
                               error_message=u'专利包失败')),
                           name='patent-package-add'),  ## 专利包提交
                       url(r'^package/(?P<pk>\d+)/edit/$',
                           login_required(PackageEditView.as_view(
                               model=PatentPackage,
                               context_object_name='patpkg',
                               template_name='rankmgr/patent_package_edit.html',
                               default_referer_url=reverse_lazy('patent-package-list'))),
                           name='patent-package-edit'),

                       url(r'package/(?P<pk>\d+)/submit/$',  # 提交一个专利包
                           login_required(DashMgrRatingPackageSubmit.as_view(
                               return_url=reverse_lazy('patent-package-list'))),
                           name='patent-package-submit'),
                       url(r'^package/(?P<pk>\d+)/data/patent/$',
                           login_required(DashMgrListJson.as_view(
                               model=PatentRatingReport,
                               initial_list=["package"],
                               columns=['name', 'department', 'count'],
                               column_template={
                                   "name": lambda o: o.patent.name,
                                   "department": lambda o: o.patent.department.name,
                                   "count": lambda o: u"%d/3" % PatentExpertRating.objects.filter(report=o).count()})),
                           name='patent-package-edit-json'),

                       url(r'package/(?P<pk>\d+)/experts/$',  # 获取某一专利的评审专家列表
                           login_required(DashMgrListJson.as_view(
                               model=PatentExpertRating, initial_list=["report"],
                               columns=['expert'],
                               column_template={"expert": lambda o: o.expert.pk})),
                           name='patent-package-patent-experts-json'),
                       url(r'package/(?P<pk>\d+)/experts/add/$',  # 增加某一专利的评审专家列表 ?patent=%d&expert=%d
                           login_required(DashMgrRatingExpertAdd.as_view(
                               model=PatentExpertRating)),
                           name='patent-package-patent-experts-add'),
                       url(r'package/(?P<pk>\d+)/experts/del/$',  # 删除某一专利的评审专家列表 ?patent=%d&expert=%d
                           login_required(DashMgrRatingExpertDel.as_view(
                               model=PatentExpertRating)),
                           name='patent-package-patent-experts-del'),  ## 专利包查看
                       url(r'^package/(?P<pk>\d+)/$',
                           login_required(PatentPackageDetailView.as_view(
                               context_object_name='patpkg',
                               template_name='rankmgr/patent_package_detail.html',
                               default_referer_url=reverse_lazy('patent-package-list'))),
                           name='patent-package-detail'),  ########## 专利评级报告 ########  # 撰写评级报告
                       url(r'package/(?P<pkgpk>\d+)/report/(?P<pk>\d+)/$',
                           login_required(PatentReportDetailView.as_view(
                               model=PatentRatingReport,
                               context_object_name='report',
                               form_class=PatentRatingReportForm,
                               template_name='rankmgr/patent_report_detail.html')),
                           name='patent-report-detail'),  ########## 专家评价界面 ########  # 待评专利列表
                       url(r'^rating/list/$',
                           login_required(PatentRatingListView.as_view(
                               context_object_name='rating_list',
                               template_name='rankmgr/patent_rating_pending_list.html')),
                           name='patent-rating-list'),
                       url(r'^rating/list/submit/$',
                           login_required(PatentRatingListView.as_view(
                               context_object_name='rating_list',
                               template_name='rankmgr/patent_rating_submit_list.html')),
                           name='submit-patent-rating-list'),
                       url(r'^rating/list/reject/$',
                           login_required(PatentRatingListView.as_view(
                               context_object_name='rating_list',
                               template_name='rankmgr/patent_rating_reject_list.html')),
                           name='reject-patent-rating-list'),

                       url(r'^rating/(?P<pk>\d+)/(?P<state>.+)/$',
                           login_required(PatentRatingDetailView.as_view(
                               model=PatentExpertRating,
                               form_class=PatentExpertRatingForm,
                               context_object_name='rating',
                               template_name='rankmgr/patent_rating_detail.html',
                               default_referer_url=reverse_lazy('patent-rating-list'),
                               success_message=u'专利 "%(name)s" 评价成功',
                               error_message=u'专利 "%(name)s" 评价失败')),
                           name='patent-rating-detail'),

                       ########### 评价导出 #############
                       # 专利评价导出
                       url(r'^export/(?P<pk>\d+)/$',
                           login_required(PatentPackageExportView.as_view()), name='patent-package-export'),
)

