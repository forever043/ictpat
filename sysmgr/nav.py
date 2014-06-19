# coding=utf-8
from django_nav import nav_groups, Nav, NavOption

class MetaMgrOption(NavOption):
    name = '基础信息管理'
    view = 'sysmgr-meta'

class BatchImportOption(NavOption):
	name = '批量数据上传'
	view = 'sysmgr-meta'

class BatchUploadOption(NavOption):
	name = '批量证书上传'
	view = 'sysmgr-meta'

class FTPOption(NavOption):
    name = '查看文件(ftp)'
    view = 'scrmgr.views.scrmgr'

class ProfileOption(NavOption):
    name = '个人信息维护'
    view = 'scrmgr.views.scrmgr'

class LoginMgrOption(NavOption):
    name = '登录安全设置'
    view = 'scrmgr.views.scrmgr'

class SysMgrNav(Nav):
    name = '系统信息维护'
    view = 'sysmgr'
    nav_group = 'main'
    options = [MetaMgrOption, BatchImportOption, BatchUploadOption, FTPOption, ProfileOption, LoginMgrOption]

nav_groups.register(SysMgrNav)

class BatchImportShortcut(Nav):
	name = '批量数据导入'
	view = 'patent-import'
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

