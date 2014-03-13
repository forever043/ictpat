# coding=utf-8
from django_nav import nav_groups, Nav, NavOption
from django.core.urlresolvers import reverse
import re

class SCRApplyOption(NavOption):
    name = '登记申请'
    view = 'scrmgr.views.scrmgr'

class SCRStateOption(NavOption):
    name = '状态维护'
    view = 'scrmgr.views.scrmgr'

class SCRListOption(NavOption):
	name = '列表查询'
	view = 'scr-list-fresh'
	regex = re.compile(r'^/dashboard/scr/(?:list|(\d+))/')
	def active_if(self, url, path):
		return self.regex.match(path)

class SCRRetvMgrOption(NavOption):
    name = '检索管理'
    view = 'scrmgr.views.scrmgr'

class SCRMgrNav(Nav):
    name = '软件著作权登记管理'
    view = 'scrmgr.views.scrmgr'
    nav_group = 'main'
    options = [SCRApplyOption, SCRStateOption, SCRListOption, SCRRetvMgrOption]

nav_groups.register(SCRMgrNav)

class SCRApplyShortcut(Nav):
	name = '软件著作权登记'
	view = 'scrmgr.views.scrmgr'
	nav_group = 'shortcut'
	template = 'dashboard/shortcut.html'
	icon = 'images/icons/pencil_48.png'

class SCRImportShortcut(Nav):
	name = '软件著作权数据导入'
	view = 'scrmgr.views.scrmgr'
	nav_group = 'shortcut'
	template = 'dashboard/shortcut.html'
	icon = 'images/icons/paper_content_pencil_48.png'

nav_groups.register(SCRApplyShortcut)
#nav_groups.register(SCRImportShortcut)

