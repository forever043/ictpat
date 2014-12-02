# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class DashboardConfig(models.Model):
    name = models.CharField(verbose_name='配置名称', max_length=64, unique=True)
    value = models.TextField(verbose_name='配置值', max_length=1024)
    memo = models.CharField(verbose_name='说明', max_length=1024, blank=True, null=True)

    def __unicode__(self):
        return self.name;

    class Meta:
        app_label = 'dashboard'
        verbose_name = u'Dashboard配置'
        verbose_name_plural = u'Dashboard配置'
        permissions = (
            ("operator", u"业务管理员权限"),
            ("expert", u"评审专家权限"),
            ("tester", u"测试用户权限"),
        )

class ExpertCatalog(models.Model):
    name = models.CharField(verbose_name='类别名', max_length=32)
    def __unicode__(self):
        return self.name;
    class Meta:
        app_label = 'dashboard'
        verbose_name = u'专家类别'
        verbose_name_plural = u'专家类别'

class ExpertProfile(models.Model):
    user = models.OneToOneField(User)
    catalog = models.ForeignKey(ExpertCatalog, verbose_name='专家类别', default=1)
    phone = models.CharField(verbose_name='联系电话', max_length=32, null=True, blank=True)
    organization = models.CharField(verbose_name='工作单位', max_length=128, null=True, blank=True)
    research_field = models.CharField(verbose_name='研究领域', max_length=128, null=True, blank=True)
    class Meta:
        app_label = 'dashboard'
        verbose_name = u'专家用户'
        verbose_name_plural = u'专家用户'
