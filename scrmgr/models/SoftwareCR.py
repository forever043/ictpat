# coding=utf-8
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from patmgr.models.Department import Department

class OverwriteStorage(FileSystemStorage):
	def get_available_name(self, name):
		if (self.exists(name)):
			self.delete(name)
		return name

fs = OverwriteStorage(location=getattr(settings, "SCR_FILE_DIRECTORY", 'files/'))

class SoftwareCR(models.Model):
	department = models.ForeignKey(Department, verbose_name=u'部门')
	name = models.CharField(max_length=128, verbose_name=u'软件名称')
	developers = models.CharField(max_length=256, verbose_name=u'完成人')
	release_date = models.DateField(verbose_name=u'首次发表时间')
	version = models.CharField(max_length=128, verbose_name=u'版本号')
	authorize_code = models.CharField(max_length=20, unique=True, verbose_name=u'软件登记号',
								error_messages={'required': '软件登记号不能为空', 'unique': '软件登记号必须唯一',})
	authorize_date = models.DateField(verbose_name=u'发证日期')
	authorize_file = models.FileField(storage=fs, upload_to='scr/authorize/', blank=True, null=True, verbose_name="软件授权证书")

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'scrmgr'

