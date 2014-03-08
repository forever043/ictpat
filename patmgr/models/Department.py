# coding=utf-8
from django.db import models

class Department(models.Model):
	name = models.CharField(max_length=40, verbose_name='部门名称')
	sort = models.IntegerField(verbose_name='排序')
	disabled = models.BooleanField(verbose_name='已关闭')
	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'patmgr'

