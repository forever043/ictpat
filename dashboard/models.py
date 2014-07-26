# coding=utf-8
from django.db import models

# Create your models here.
class DashboardConfig(models.Model):
	name = models.CharField(verbose_name='配置名称', max_length=64, unique=True)
	value = models.CharField(verbose_name='配置值', max_length=1024)
	memo = models.CharField(verbose_name='说明', max_length=1024, blank=True, null=True)

	def __unicode__(self):
		return self.name;

	class Meta:
		app_label = 'dashboard'
		verbose_name = u'Dashboard配置'
		verbose_name_plural = u'Dashboard配置'
		permissions = (
			("operator", u"业务管理员权限"),
			("expert", u"评审专家权限"),
			("tester", u"测试用户权限"),
		)

