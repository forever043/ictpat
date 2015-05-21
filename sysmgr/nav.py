# coding=utf-8
from django_nav import nav_groups, Nav, NavOption
from django_nav.conditionals import *

class MetaMgrOption(NavOption):
	name = '基础信息管理'
	view = 'sysmgr-meta'
	conditional = {
		'function': user_has_perm,
		'args': [],
		'kwargs': { 'perm': 'rankmgr.can_operate_package' },
	}

class BatchImportOption(NavOption):
	name = '批量数据导入'
	view = 'sysmgr-import'
	conditional = {
		'function': user_has_perm,
		'args': [],
		'kwargs': { 'perm': 'rankmgr.can_operate_package' },
	}

class BatchUploadOption(NavOption):
	name = '批量证书上传'
	view = 'sysmgr-upload'
	conditional = {
		'function': user_has_perm,
		'args': [],
		'kwargs': { 'perm': 'rankmgr.can_operate_package' },
	}

class FTPOption(NavOption):
	name = '查看文件(ftp)'
	view = 'scrmgr.views.scrmgr'
	conditional = {
		'function': user_has_perm,
		'args': [],
		'kwargs': { 'perm': 'rankmgr.can_operate_package' },
	}

class ProfileOption(NavOption):
	name = '个人信息维护'
	view = 'sysmgr-profile'

class LoginMgrOption(NavOption):
	name = '修改密码'
	view = 'sysmgr-profile'

class SysMgrNav(Nav):
	name = '系统信息维护'
	view = 'sysmgr'
	nav_group = 'main'
	options = [MetaMgrOption, BatchImportOption, BatchUploadOption, FTPOption, ProfileOption]

nav_groups.register(SysMgrNav)

class BatchImportShortcut(Nav):
	name = '批量数据导入'
	view = 'sysmgr-import'
	nav_group = 'shortcut'
	template = 'dashboard/shortcut.html'
	icon = 'images/icons/paper_content_pencil_48.png'

class LicenseFileMgrShortcut(Nav):
	name = '证书文件管理'
	view = 'patent-file'
	nav_group = 'shortcut'
	template = 'dashboard/shortcut.html'
	icon = 'images/icons/image_add_48.png'

class RankMgrShortcut(Nav):
	name = '知识产权评级管理'
	view = 'patent-package-list'
	nav_group = 'shortcut'
	template = 'dashboard/shortcut.html'
	icon = 'images/icons/clock_48.png'

nav_groups.register(BatchImportShortcut)
nav_groups.register(LicenseFileMgrShortcut)
nav_groups.register(RankMgrShortcut)

