# coding=utf-8
from django_nav import nav_groups, Nav, NavOption
from django.core.urlresolvers import reverse
import re

class SCRApplyOption(NavOption):
    name = '登记申请'
    view = 'scr-add'

class SCRListOption(NavOption):
	name = '列表查询'
	view = 'scr-list-fresh'
	regex = re.compile(r'^/dashboard/scr/(?:list|(\d+))/')
	def active_if(self, url, path):
		return self.regex.match(path)

class SCRImportOption(NavOption):
	name = '软件登记数据导入'
	view = 'scr-import'

class SCRFileUploadOption(NavOption):
	name = '软件登记证书上传'
	view = 'scr-file'

class SCRRetrvMgrOption(NavOption):
    name = '检索方案管理'
    view = 'scr-retrvscheme'

class SCRMgrNav(Nav):
    name = '软件著作权登记管理'
    view = 'scrmgr.views.scrmgr'
    nav_group = 'main'
    options = [SCRApplyOption, SCRListOption, SCRImportOption, SCRFileUploadOption, SCRRetrvMgrOption]

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

