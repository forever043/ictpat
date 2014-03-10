# coding=utf-8
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from patmgr.models.Department import Department

class PatentState(models.Model):
	name = models.CharField(max_length=40, verbose_name=u'专利状态')
	sort = models.IntegerField(verbose_name=u'排序')
	disabled = models.BooleanField(verbose_name=u'已关闭')
	def __unicode__(self):
		return self.name
	class Meta:
		app_label = 'patmgr'


class PatentType(models.Model):
	name = models.CharField(max_length=40, verbose_name=u'专利类型')
	sort = models.IntegerField(verbose_name=u'排序')
	disabled = models.BooleanField(verbose_name=u'已关闭')
	def __unicode__(self):
		return self.name
	class Meta:
		app_label = 'patmgr'


class OverwriteStorage(FileSystemStorage):
	def get_available_name(self, name):
		if (self.exists(name)):
			self.delete(name)
		return name

fs = OverwriteStorage(location=getattr(settings, "PATENT_FILE_DIRECTORY", 'files/'))

class Patent(models.Model):
	name = models.CharField(max_length=128, verbose_name=u'专利名称')
	department = models.ForeignKey(Department, verbose_name=u'部门')
	inventors = models.CharField(max_length=256, verbose_name=u'发明人')
	type = models.ForeignKey(PatentType, verbose_name=u'专利类型')
	state = models.ForeignKey(PatentState, verbose_name=u'专利状态')
	apply_code = models.CharField(max_length=20, unique=True, verbose_name=u'申请号', error_messages={'required': '申请号不能为空', 'unique': '申请号必须唯一',})
	apply_date = models.DateField(verbose_name=u'申请时间')
	authorize_code = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'授权号')
	authorize_date = models.DateField(blank=True, null=True, verbose_name=u'授权时间')
	apply_file = models.FileField(storage=fs, upload_to='patent/apply/', blank=True, null=True, verbose_name="专利受理证书")
	authorize_file = models.FileField(storage=fs, upload_to='patent/authorize/', blank=True, null=True, verbose_name="专利授权证书")
	
	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'patmgr'

