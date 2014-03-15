# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

from scrmgr.models import SoftwareCR

class SoftwareCRRank(models.Model):
	scr    = models.ForeignKey(SoftwareCR, verbose_name=u'软件')
	expert = models.ForeignKey(User, verbose_name=u'评分专家')
	rank   = models.IntegerField(verbose_name=u'评分')
	remark = models.TextField(verbose_name=u'评语')
	
	def __unicode__(self):
		return self.expert.last_name + self.expert.first_name

	class Meta:
		app_label = 'scrmgr'
		unique_together=(("scr", "expert"),)

