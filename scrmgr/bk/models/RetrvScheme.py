# coding=utf-8
from django.db import models

from scrmgr.models import SoftwareExtFieldType, Software

class RetrvScheme(models.Model):
	name = models.CharField(max_length=128, verbose_name="检索方案名称")
	current = models.BooleanField(verbose_name="当前方案")
	def __unicode__(self):
		return self.name
	class Meta:
		app_label = "scrmgr"
		verbose_name = "检索方案"

class BuiltinRetrvField(models.Model):
	scheme = models.ForeignKey(RetrvScheme, verbose_name="检索方案")
	field_name = models.CharField(max_length=128, verbose_name="检索字段名称")
	retrieve = models.BooleanField(verbose_name="可检索")
	display = models.BooleanField(verbose_name="列表显示")
	sort = models.IntegerField(verbose_name="排序")

	def __unicode__(self):
		return u"%s: %s" % (self.scheme.name, Software._meta.get_field(self.field_name).verbose_name)
	class Meta:
		app_label = "scrmgr"
		verbose_name = u"内建检索字段"
	unique_together=(("scheme", "field_name"),)

class CustomizedRetrvField(models.Model):
	scheme = models.ForeignKey(RetrvScheme, verbose_name="检索方案")
	field = models.ForeignKey(SoftwareExtFieldType, verbose_name="检索字段")
	retrieve = models.BooleanField(verbose_name="可检索")
	display = models.BooleanField(verbose_name="列表显示")
	sort = models.IntegerField(verbose_name="排序")
	
	def __unicode__(self):
		return (u"%s: %s") % (self.scheme.name, self.field.field_label)
	class Meta:
		app_label = "scrmgr"
		verbose_name = u"自定义检索字段"
	unique_together=(("scheme", "field"),)

