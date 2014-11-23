# coding=utf-8
from django.db import models

from patmgr.models import Patent

class PatentExtFieldType(models.Model):
    field_name = models.CharField(unique=True, max_length=128, verbose_name='扩展字段类型名')
    field_label = models.CharField(max_length=123, verbose_name='扩展字段类型标签')
    retrieval = models.BooleanField(verbose_name='检索字段')
    disabled = models.BooleanField(verbose_name='已关闭')
    sort = models.IntegerField(verbose_name='排序值')
    def __unicode__(self):
        return self.field_label
    class Meta:
        app_label = 'patmgr'
        verbose_name = u'专利扩展字段类型'
        verbose_name_plural = u'专利扩展字段类型'


class PatentExtField(models.Model):
    patent = models.ForeignKey(Patent, verbose_name='专利')
    type = models.ForeignKey(PatentExtFieldType, verbose_name='扩展字段类型')
    value = models.CharField(max_length=512, verbose_name='扩展字段值')
    def __unicode__(self):
        return self.value
    class Meta:
        app_label = 'patmgr'
        verbose_name = u'专利扩展字段数据'
        verbose_name_plural = u'专利扩展字段数据'
	unique_together=(("patent", "type"),)

