# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.encoding import smart_unicode
from retrvhome.dynamic_models_tool import create_dynamic_model

class PatentField(models.Model):
	field_name = models.CharField(unique=True, max_length=128, verbose_name='扩展字段类型名')
	field_label = models.CharField(max_length=123, verbose_name='扩展字段类型标签')
	display = models.BooleanField(verbose_name='列表显示')
	retrieve = models.BooleanField(verbose_name='检索字段')
	sort = models.IntegerField(verbose_name='排序值')
	def __unicode__(self):
		return self.field_label

# Create retrieve patent model
fields = { '__unicode__': lambda self: smart_unicode(self.name) }
try:
	for f in PatentField.objects.all():
		fields[f.field_name] = models.CharField(max_length=512, verbose_name=f.field_label)
except:
	pass
Patent = create_dynamic_model(modelname = "Patent",
					 app_label = "retrvhome",
					 module = "retrvhome.models",
					 options = {"verbose_name": u"检索专利", "verbose_name_plural": u"检索专利"},
					 admin_options = {},
					 fields = fields)

