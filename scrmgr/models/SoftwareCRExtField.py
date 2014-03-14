# coding=utf-8
from django.db import models

from scrmgr.models import SoftwareCR

class SoftwareCRExtFieldType(models.Model):
    field_name = models.CharField(unique=True, max_length=128, verbose_name=u'扩展字段类型名')
    field_label = models.CharField(max_length=123, verbose_name=u'扩展字段类型标签')
    retrieval = models.BooleanField(verbose_name=u'检索字段')
    disabled = models.BooleanField(verbose_name=u'已关闭')
    sort = models.IntegerField(verbose_name=u'排序值')
    def __unicode__(self):
        return self.field_label
    class Meta:
        app_label = 'scrmgr'


class SoftwareCRExtField(models.Model):
    scr = models.ForeignKey(SoftwareCR, verbose_name=u'软件登记')
    type = models.ForeignKey(SoftwareCRExtFieldType, verbose_name=u'扩展字段类型')
    value = models.CharField(max_length=512, verbose_name=u'扩展字段值')
    def __unicode__(self):
        return self.value
    class Meta:
        app_label = 'scrmgr'
	unique_together=(("scr", "type"),)

