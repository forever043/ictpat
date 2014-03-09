# coding=utf-8
from django.db import models

from patmgr.models import PatentExtFieldType

class RetrvSchema(models.Model):
	name = models.CharField(max_length=128, verbose_name="检索方案名称")
	current = models.BooleanField(verbose_name="当前方案")
	def __unicode__(self):
		return self.name
	class Meta:
		app_label = "patmgr"

class RetrvBuiltinField(models.Model):
	schema = models.ForeignKey(RetrvSchema, verbose_name="检索方案")
	field_name = models.CharField(max_length=128, verbose_name="检索字段名称")
	retrieve = models.BooleanField(verbose_name="可检索")
	display = models.BooleanField(verbose_name="列表显示")
	sort = models.IntegerField(verbose_name="排序")

	def __unicode__(self):
		return "%s: %s" % self.schema.name, self.field_name
	class Meta:
		app_label = "patmgr"
	unique_together=(("schema", "field_name"),)

class RetrvCustomizeField(models.Model):
	schema = models.ForeignKey(RetrvSchema, verbose_name="检索方案")
	field = models.ForeignKey(PatentExtFieldType, verbose_name="检索字段")
	retrieve = models.BooleanField(verbose_name="可检索")
	display = models.BooleanField(verbose_name="列表显示")
	sort = models.IntegerField(verbose_name="排序")
	
	def __unicode__(self):
		return "%s: %s" % self.schema.name, self.field.name
	class Meta:
		app_label = "patmgr"
	unique_together=(("schema", "field"),)

