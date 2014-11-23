# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

from dashboard.models import ExpertCatalog
from patmgr.models import Patent
from rankmgr.models.RankItem import RankItem, RankOption, RankCatalog

class PatentPackage(models.Model):
    name = models.CharField(verbose_name='专利包名称', max_length=100, unique=True)
    rating_weight = models.CommaSeparatedIntegerField(verbose_name='评分权重', max_length=20,
                                                      default='2,2,2,2,2')
    submit_date = models.DateField(verbose_name='提交时间', null=True, blank=True)
    finish_date = models.DateField(verbose_name='完成时间', null=True, blank=True)
    def __unicode__(self):
        return self.name;
    class Meta:
        app_label = 'rankmgr'
        verbose_name = u'专利包'
        verbose_name_plural = u'专利包'
        permissions = (("can_operate_package", u"可以操作专利包"),)

class PatentPackageRankItem(models.Model):
    package = models.ForeignKey(PatentPackage, verbose_name='专利包')
    item = models.ForeignKey(RankItem, verbose_name='评分项目')
    weight = models.IntegerField(verbose_name='权重')
    
    def __unicode__(self):
        return u"[%s][%s]%s" % (self.package.name, self.item.catalog.name, self.item.desc)
    class Meta:
        app_label = 'rankmgr'
        verbose_name = u'专利包评分项目'
        verbose_name_plural = u'专利包评分项目'
        unique_together=(("package", "item"),)

class ExpertCatalogWeight(models.Model):
    package = models.ForeignKey(PatentPackage, verbose_name='专利包')
    expert_catalog = models.ForeignKey(ExpertCatalog, verbose_name='专家类别')
    rank_catalog = models.ForeignKey(RankCatalog, verbose_name='评分项目类别')
    weight = models.IntegerField(verbose_name='权重')

    def __unicode__(self):
        return u'[%s][%s<-%s] %d' % (self.package.name, self.rank_catalog.name, self.expert_catalog.name, self.weight)
    class Meta:
        app_label = 'rankmgr'
        verbose_name = u'专家类别权重'
        verbose_name_plural = u'专家类别权重'
        unique_together=(("package", "expert_catalog", "rank_catalog"),)

class PatentRatingReport(models.Model):
    package = models.ForeignKey(PatentPackage, verbose_name='专利包')
    patent = models.ForeignKey(Patent, verbose_name='专利')
    rating = models.IntegerField(verbose_name='综合分', null=True, blank=True)
    rank = models.IntegerField(verbose_name='等级', null=True, blank=True)
    report = models.TextField(verbose_name='评级报告', null=True, blank=True)
    finish_date = models.DateField(verbose_name='完成时间', null=True, blank=True)
    def __unicode__(self):
        return u"[%s]%s" % (self.package.name, self.patent.name)
    class Meta:
        app_label = 'rankmgr'
        verbose_name = u'专利评级报告'
        verbose_name_plural = u'专利评级报告'


class PatentExpertItemRating(models.Model):
    report = models.ForeignKey(PatentRatingReport, verbose_name='所属评级报告')
    expert = models.ForeignKey(User, verbose_name='专家')
    rankitem = models.ForeignKey(PatentPackageRankItem, verbose_name='评分项目')
    select = models.ForeignKey(RankOption, verbose_name='选择', null=True, blank=True)
    def __unicode__(self):
        return u"[%s][%s]<%s%s:%d> [%s]%s" % (self.rankitem.package.name, self.report.patent.name, self.expert.last_name, self.expert.first_name, self.select.index, self.rankitem.item.catalog.name, self.rankitem.item.desc)
    class Meta:
        app_label = 'rankmgr'
        verbose_name = u'专家评分表(old)'
        verbose_name_plural = u'专家评分表(old)'
        unique_together=(("report", "expert", "rankitem"),)


class PatentExpertRating(models.Model):
    report = models.ForeignKey(PatentRatingReport, verbose_name='所属评级报告')
    expert = models.ForeignKey(User, verbose_name='评分专家')
    ratings = models.CommaSeparatedIntegerField(verbose_name='专家评分', max_length=15, default='0,0,0,0,0')
    remark = models.TextField(verbose_name='专家意见', null=True, blank=True)
    submit_date = models.DateField(verbose_name='提交时间', null=True, blank=True)
    def __unicode__(self):
        return u"%s: %s[%s]" % (self.report.package.name, self.report.patent.name, self.expert.last_name + self.expert.first_name)
    class Meta:
        app_label = 'rankmgr'
        verbose_name = u'专家评分'
        verbose_name_plural = u'专家评分'
        unique_together=(("report", "expert"),)
        permissions = (("can_operate_rating", u"可以操作专利评价"),)

