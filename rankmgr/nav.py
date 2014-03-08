# coding=utf-8
from django_nav import nav_groups, Nav, NavOption

class SummaryOption(NavOption):
    name = '知识产权评级统计'
    view = 'scrmgr.views.scrmgr'

class PATRankOption(NavOption):
    name = '专利等级评定'
    view = 'scrmgr.views.scrmgr'

class SCRRankOption(NavOption):
    name = '软件等级评定'
    view = 'scrmgr.views.scrmgr'

class ExpertMgrOption(NavOption):
    name = '专家管理'
    view = 'scrmgr.views.scrmgr'

class RankMgrNav(Nav):
    name = '知识产权等级评定'
    view = 'scrmgr.views.scrmgr'
    nav_group = 'main'
    options = [SummaryOption, PATRankOption, SCRRankOption, ExpertMgrOption]

nav_groups.register(RankMgrNav)
