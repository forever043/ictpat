# -*- coding: UTF-8 -*-
import csv
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.views.generic import View

from rankmgr.models import *

class CSVResponseMixin(object):
	"""
	A generic mixin that constructs a CSV response from the context data if
	the CSV export option was provided in the request.
	"""
	def render_to_response(self, context, **response_kwargs):
		"""
		Creates a CSV response if requested, otherwise returns the default
		template response.
		"""
		# Sniff if we need to return a CSV export
		response = HttpResponse(content_type='text/csv')
		response.write('\xEF\xBB\xBF')
		response['Content-Disposition'] = u'attachment; filename="%s.csv"' % context['title']

		writer = csv.writer(response, dialect='excel')
		# Write the data from the context somehow
		for item in context['items']:
			writer.writerow([o.encode('utf8') for o in item])
		return response

class PatentPackageExportView(View, CSVResponseMixin):
	def get(self, request, *args, **kwargs):
		pk = kwargs['pk']
		context = {
			"title": "export2014",
			"items": [[u'专利名称', u'部门', u'发明人', u'专家1', u'评分1', u'评价1', u'专家2', u'评分2', u'评价2', u'专家3', u'评分3', u'评价3']]
		}
		for report in PatentRatingReport.objects.filter(package__pk=pk):
			column = [report.patent.name, report.patent.department.name, report.patent.inventors]
			for rating in PatentExpertRating.objects.filter(patent=report):
				column.append(u"%s%s" % (rating.expert.last_name, rating.expert.first_name))
				column.append(u"%d" % rating.rank if rating.rank else "----")
				column.append(rating.remark if rating.remark else "----")
			context["items"].append(column)
		return self.render_to_response(context)

