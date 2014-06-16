# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

from patmgr.models import Patent

class PatentRank(models.Model):
	patent = models.ForeignKey(Patent, verbose_name='专利')
	expert = models.ForeignKey(User, verbose_name='评分专家')
	rank = models.IntegerField(verbose_name='评分')
	remark = models.TextField(verbose_name='评语')
	
	def __unicode__(self):
		return self.expert.last_name + self.expert.first_name
	class Meta:
		app_label = 'patmgr'
		unique_together=(("patent", "expert"),)

