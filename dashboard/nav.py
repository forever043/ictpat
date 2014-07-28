# coding=utf-8
from django_nav import nav_groups, Nav, NavOption
from django_nav.conditionals import *

class DashboardNav(Nav):
    name = 'Dashboard'
    view = 'dashboard'
    nav_group = 'main'
    conditional = {
        'function': user_has_perm,
        'args': [],
        'kwargs': { 'perm': 'rankmgr.can_operate_package' },
    }

nav_groups.register(DashboardNav)

