# coding=utf-8
from django_nav import nav_groups, Nav, NavOption

class DashboardNav(Nav):
    name = 'Dashboard'
    view = 'dashboard'
    nav_group = 'main'

nav_groups.register(DashboardNav)

