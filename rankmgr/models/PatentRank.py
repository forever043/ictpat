# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

from patmgr.models import Patent

class PatentPackage(models.Model):
	name = models.CharField(verbose_name='专利包名称', max_length=100, unique=True)
	submit_date = models.DateField(verbose_name='提交时间', null=True, blank=True)
	finish_date = models.DateField(verbose_name='完成时间', null=True, blank=True)
	def __unicode__(self):
		return self.name;
	class Meta:
		app_label = 'rankmgr'
		verbose_name = u'专利包'
		verbose_name_plural = u'专利包'
		permissions = (("can_operate_package", u"可以操作专利包"),)

class PatentRatingReport(models.Model):
	package = models.ForeignKey(PatentPackage, verbose_name='专利包')
	patent = models.ForeignKey(Patent, verbose_name='专利')
	rating = models.IntegerField(verbose_name='综合分', null=True, blank=True)
	rank = models.IntegerField(verbose_name='等级', null=True, blank=True)
	report = models.TextField(verbose_name='评级报告', null=True, blank=True)
	finish_date = models.DateField(verbose_name='完成时间', null=True, blank=True)
	def __unicode__(self):
		return u"[%s]%s" % (self.package.name, self.patent.name)
	class Meta:
		app_label = 'rankmgr'
		verbose_name = u'专利评级报告'
		verbose_name_plural = u'专利评级报告'

class PatentExpertRating(models.Model):
	report = models.ForeignKey(PatentRatingReport, verbose_name='所属评级报告')
	expert = models.ForeignKey(User, verbose_name='评分专家')
	ratings = models.CommaSeparatedIntegerField(verbose_name='专家评分', max_length=15, default='0,0,0,0,0')
	remark = models.TextField(verbose_name='专家意见', null=True, blank=True)
	submit_date = models.DateField(verbose_name='提交时间', null=True, blank=True)
	def __unicode__(self):
		return u"%s: %s[%s]" % (self.report.package.name, self.report.patent.name, self.expert.last_name + self.expert.first_name)
	class Meta:
		app_label = 'rankmgr'
		verbose_name = u'专家评分'
		verbose_name_plural = u'专家评分'
		unique_together=(("report", "expert"),)
		permissions = (("can_operate_rating", u"可以操作专利评价"),)

