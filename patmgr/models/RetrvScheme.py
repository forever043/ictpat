# coding=utf-8
from django.db import models

from patmgr.models import PatentExtFieldType, Patent

class RetrvScheme(models.Model):
	name = models.CharField(max_length=128, verbose_name=u"检索方案名称")
	current = models.BooleanField(verbose_name=u"当前方案")
	def __unicode__(self):
		return self.name
	class Meta:
		app_label = "patmgr"
		verbose_name = "检索方案"

class BuiltinRetrvField(models.Model):
	INPUT_TYPE = 'TX'
	OPTION_TYPE = 'OP'
	RETRIEVE_TYPES = (
		(INPUT_TYPE, 'Input'),
		(OPTION_TYPE, 'Option'),
	)
	scheme = models.ForeignKey(RetrvScheme, verbose_name=u"检索方案")
	field_name = models.CharField(max_length=128, verbose_name=u"检索字段名称")
	retrieve = models.BooleanField(verbose_name=u"可检索")
	display = models.BooleanField(verbose_name=u"列表显示")
	sort = models.IntegerField(verbose_name=u"排序")
	type = models.CharField(max_length=2, verbose_name=u"检索类型", choices=RETRIEVE_TYPES, default=INPUT_TYPE)

	def __unicode__(self):
		#return u"%s: %s" % (self.scheme.name, Patent._meta.get_field(self.field_name).verbose_name)
		return Patent._meta.get_field(self.field_name).verbose_name
	class Meta:
		app_label = "patmgr"
		verbose_name = u"内建检索字段"
	unique_together=(("scheme", "field_name"),)

class CustomizedRetrvField(models.Model):
	INPUT_TYPE = 'TX'
	OPTION_TYPE = 'OP'
	RETRIEVE_TYPES = (
		(INPUT_TYPE, 'Input'),
		(OPTION_TYPE, 'Option'),
	)
	scheme = models.ForeignKey(RetrvScheme, verbose_name=u"检索方案")
	field = models.ForeignKey(PatentExtFieldType, verbose_name=u"检索字段")
	retrieve = models.BooleanField(verbose_name=u"可检索")
	display = models.BooleanField(verbose_name=u"列表显示")
	sort = models.IntegerField(verbose_name=u"排序")
	type = models.CharField(max_length=2, verbose_name=u"检索类型", choices=RETRIEVE_TYPES, default=INPUT_TYPE)
	
	def __unicode__(self):
		return (u"%s: %s") % (self.scheme.name, self.field.field_label)
	class Meta:
		app_label = "patmgr"
		verbose_name = u"自定义检索字段"
	unique_together=(("scheme", "field"),)

