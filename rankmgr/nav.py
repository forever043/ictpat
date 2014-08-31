# coding=utf-8
from django_nav import nav_groups, Nav, NavOption
from django_nav.conditionals import *
import re


class PATPackageOption(NavOption):
    name = '专利评价包管理'
    view = 'patent-package-list'
    conditional = {
        'function': user_has_perm,
        'args': [],
        'kwargs': {'perm': 'rankmgr.can_operate_package'},
    }


class PATRatingOption(NavOption):
    name = '待评专利列表'
    view = 'patent-rating-list'
    conditional = {
        'function': user_has_perm,
        'args': [],
        'kwargs': {'perm': 'rankmgr.can_operate_rating'},
    }
    regex = re.compile(r'^/dashboard/rank/rating/(?:list|(\d+/pending))/$')

    def active_if(self, url, path):
        return self.regex.match(path)


class PATSubmittedRatingOption(NavOption):
    name = '已评价专利列表'
    view = 'submit-patent-rating-list'
    conditional = {
        'function': user_has_perm,
        'args': [],
        'kwargs': {'perm': 'rankmgr.can_operate_rating'},
    }
    regex = re.compile(r'^/dashboard/rank/rating/(?:list/submit|(\d+/submit))/')

    def active_if(self, url, path):
        print url
        print path
        return self.regex.match(path)


class PATRejectedRatingOption(NavOption):
    name = '已拒绝专利列表'
    view = 'reject-patent-rating-list'
    conditional = {
        'function': user_has_perm,
        'args': [],
        'kwargs': {'perm': 'rankmgr.can_operate_rating'},
    }
    regex = re.compile(r'^/dashboard/rank/rating/(?:list/reject|(\d+/reject))/')

    def active_if(self, url, path):
        return self.regex.match(path)


class SummaryOption(NavOption):
    name = '知识产权评级统计'
    view = 'rank-summary'
    conditional = {'function': user_is_staff, 'args': [], 'kwargs': {}}


class ExpertMgrOption(NavOption):
    name = '专家管理'
    view = 'rank-expert-list'
    conditional = {
        'function': user_has_perm,
        'args': [],
        'kwargs': {'perm': 'rankmgr.can_operate_package'},
    }


class RankMgrNav(Nav):
    name = '知识产权等级评定'
    view = 'rank'
    nav_group = 'main'
    options = [PATPackageOption, PATRatingOption, PATSubmittedRatingOption, PATRejectedRatingOption, SummaryOption,
               ExpertMgrOption]


nav_groups.register(RankMgrNav)

