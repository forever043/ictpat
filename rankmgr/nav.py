# coding=utf-8
from django_nav import nav_groups, Nav, NavOption

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
    options = [SummaryOption, ExpertMgrOption]

nav_groups.register(RankMgrNav)
