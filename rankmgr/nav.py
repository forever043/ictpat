# coding=utf-8
from django_nav import nav_groups, Nav, NavOption
import re

class PATPackageOption(NavOption):
	name = '专利评价包管理'
	view = 'patent-package-list'

class PATRatingOption(NavOption):
	name = '待评专利列表'
	view = 'patent-rating-list'
	regex = re.compile(r'^/dashboard/rank/rating/(?:list|(\d+))/')
	def active_if(self, url, path):
		return self.regex.match(path)

class SummaryOption(NavOption):
    name = '知识产权评级统计'
    view = 'rank-summary'

class ExpertMgrOption(NavOption):
    name = '专家管理'
    view = 'rank-expert-list'

class RankMgrNav(Nav):
    name = '知识产权等级评定'
    view = 'rank'
    nav_group = 'main'
    options = [PATPackageOption, PATRatingOption, SummaryOption, ExpertMgrOption]

nav_groups.register(RankMgrNav)

