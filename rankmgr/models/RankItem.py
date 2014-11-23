# coding=utf-8
# 评分项目库
from django.db import models

class RankCatalog(models.Model):
	name = models.CharField(verbose_name='评分项目类别', max_length=20, unique=True)
	desc = models.CharField(verbose_name='评分项目类别描述', max_length=200, null=True, blank=True)

	def __unicode__(self):
		return self.name
	class Meta:
		app_label = 'rankmgr'
		verbose_name = u'评分项目类别'
		verbose_name_plural = u'评分项目类别'

class RankOption(models.Model):
	name = models.CharField(verbose_name='选项', max_length=10, unique=True)
	index = models.IntegerField(verbose_name='序号', unique=True)

	def __unicode__(self):
		return self.name
	class Meta:
		app_label = 'rankmgr'
		verbose_name = u'评分选项'
		verbose_name_plural = u'评分选项'


class RankItem(models.Model):
	catalog = models.ForeignKey(RankCatalog, verbose_name='项目类别')
	desc = models.CharField(verbose_name='项目描述', max_length=200)
	optNr = models.IntegerField(verbose_name='选项数目', default=1)
	optA = models.CharField(verbose_name='选项A', max_length=100)
	optB = models.CharField(verbose_name='选项B', max_length=100, blank=True, null=True)
	optC = models.CharField(verbose_name='选项C', max_length=100, blank=True, null=True)
	optD = models.CharField(verbose_name='选项D', max_length=100, blank=True, null=True)
	optE = models.CharField(verbose_name='选项E', max_length=100, blank=True, null=True)
	optF = models.CharField(verbose_name='选项F', max_length=100, blank=True, null=True)

	def __unicode__(self):
		return u'[%s] %s' % (self.catalog.name, self.desc);
	class Meta:
		app_label = 'rankmgr'
		verbose_name = u'评分项目'
		verbose_name_plural = u'评分项目'

