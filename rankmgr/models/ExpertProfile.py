# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

class ExpertProfile(models.Model):
	phone = models.CharField(verbose_name='联系电话', max_length=32, null=True, blank=True)
	organization = models.CharField(verbose_name='工作单位', max_length=128, null=True, blank=True)
	research_field = models.CharField(verbose_name='研究领域', max_length=128, null=True, blank=True)
	user = models.ForeignKey(User, unique=True)
	class Meta:
		app_label = 'rankmgr'
		verbose_name = u'专家信息'
		verbose_name_plural = u'专家信息'

