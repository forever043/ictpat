# -*- coding: UTF-8 -*-
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.core import exceptions
import json
import string

from rankmgr.models import *

def get_all_rank_catalog():
	return RankCatalog.objects.filter(disabled=False).order_by('sort')

def get_package_rank_catalog(package):
	return [package_catalog.catalog for package_catalog in PatentPackageCatalogWeight.objects.filter(package=package)]

def get_package_rank_catalog_item(package, catalog):
	return PatentPackageRankItem.objects.filter(package=package, item__catalog=catalog)

def get_package_rank_item(package):
	return PatentPackageRankItem.objects.filter(package=package)

def get_rating_finished(rating):
	return RatingSelect.objects.filter(rating=rating)

def get_package_catalog_rating_score(catalog, rating):
	score = PatentPackageCatalogWeight.objects.get(package=rating.report.package, catalog=catalog).weight
	weighted_item_list = PatentPackageRankItem.objects.filter(package=rating.report.package, item__catalog=catalog)

	count = len(PatentPackageRankItem.objects.filter(package=rating.report.package, item__catalog=catalog))
	finish_count = len(RatingSelect.objects.filter(rating=rating, item__catalog=catalog))
	if not count == finish_count:
		return -1

	total_weight = 0
	for weighted_item in weighted_item_list:
		total_weight += weighted_item.weight

	final_score = 0
	for weighted_item in weighted_item_list:
		item_score = float(score * weighted_item.weight)/total_weight
		select_index = RatingSelect.objects.get(rating=rating, item=weighted_item.item).select.index
		select_percent = float(weighted_item.item.optNr - select_index)/weighted_item.item.optNr
		final_score += item_score * select_percent

	return final_score

def get_package_rating_score(rating):
	final_score = 0
	for catalog in get_package_rank_catalog(rating.report.package):
		score = get_package_catalog_rating_score(catalog, rating)
		if score == -1:
			return -1
		final_score += score
	return final_score

def get_package_score(package):
	pass
