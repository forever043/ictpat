# coding=utf-8
from django_nav import nav_groups, Nav, NavOption
from django.core.urlresolvers import reverse
from django_nav.conditionals import *
import re

class PATApplyOption(NavOption):
	name = '登记申请'
	view = 'patent-add'

class PATListOption(NavOption):
	name = '列表查询'
	view = 'patent-list-fresh'
	regex = re.compile(r'^/dashboard/patent/(?:list|(\d+))/')

	def active_if(self, url, path):
		return self.regex.match(path)

class PATRetvMgrOption(NavOption):
	name = '检索方案管理'
	view = 'patent-retrvscheme'

class PATExtFieldMgrOption(NavOption):
	name = '扩展属性管理'
	view = 'patent-extfield'

class PATImportOption(NavOption):
	name = '专利数据导入'
	view = 'patent-import'

class PATFileUploadOption(NavOption):
	name = '专利证书上传'
	view = 'patent-file'

class PATMgrNav(Nav):
	name = '专利信息维护'
	view = 'patent'
	nav_group = 'main'
	options = [PATApplyOption, PATListOption, PATImportOption, PATFileUploadOption, PATExtFieldMgrOption, PATRetvMgrOption]
	conditional = {
		'function': user_has_perm,
		'args': [],
		'kwargs': { 'perm': 'rankmgr.can_operate_package' },
	}

nav_groups.register(PATMgrNav)

class PATApplyShortcut(Nav):
	name = '专利申请登记'
	view = 'patent-add'
	nav_group = 'shortcut'
	template = 'dashboard/shortcut.html'
	icon = 'images/icons/pencil_48.png'

class PATImportShortcut(Nav):
	name = '专利数据导入'
	view = 'patent-import'
	nav_group = 'shortcut'
	template = 'dashboard/shortcut.html'
	icon = 'images/icons/paper_content_pencil_48.png'

nav_groups.register(PATApplyShortcut)
#nav_groups.register(PATImportShortcut)

