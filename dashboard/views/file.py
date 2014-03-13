# coding=utf-8
import os
from django.http import HttpResponse
from django.http import Http404
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.db.models import Q
from django.db import IntegrityError, DatabaseError
from django.core import exceptions
from django.core.exceptions import ObjectDoesNotExist
from filetransfers.api import serve_file
import json

from patmgr.models import Patent

class FileServeView(View):
	model = None
	fcode_map = {}

	def get(self, request, *args, **kwargs):
		if not self.model or not self.fcode_map:
			raise Http404
		
		q = Q()
		file = None
		fcode = kwargs["fcode"]

		for code_attr, file_attr in self.fcode_map.iteritems():
			q |= Q((code_attr, fcode))
		match_entry = self.model.objects.filter(q)
		if not match_entry or not len(match_entry)==1:
			raise Http404

		entry = match_entry[0]
		for code_attr, file_attr in self.fcode_map.iteritems():
			if getattr(entry, code_attr) == fcode:
				file = getattr(entry, file_attr)
				break
		if not file:
			raise Http404
		return serve_file(request, file, save_as=False)

class FileUploadView(View):
	model = None
	fcode_map = {}

	def get(self, request, *args, **kwargs):
		return HttpResponse('')

	def post(self, request, *args, **kwargs):
		files = []
		for field, file in request.FILES.iteritems():
			file_entry = {"name": file.name, "size": file.size}

			fcode, ext = os.path.splitext(file.name)

			q = Q()
			for code_attr, file_attr in self.fcode_map.iteritems():
				q |= Q((code_attr, fcode))
			match_entry = self.model.objects.filter(q)

			if not match_entry:
				file_entry["error"] = u"无对应专利"
			elif len(match_entry) > 1:
				file_entry["error"] = u"专利数据库中申请号或授权号不唯一：%s" % fcode
			else:
				entry = match_entry[0]
				for code_attr, file_attr in self.fcode_map.iteritems():
					if getattr(entry, code_attr) == fcode:
						setattr(entry, file_attr, file)
						file_entry["name"] = u"申请文件：%s" % entry.name
						file_entry["url"] = reverse("patent-file-service", args=(getattr(entry, code_attr),))
						break
				entry.save()
				file_entry["thumbnailUrl"] = "/resources/images/icon_pdf.png"
				file_entry["deleteUrl"] = file_entry["url"]
				file_entry["deleteType"] = "DELETE"
			files.append(file_entry);
		return HttpResponse(json.dumps({"files": files}), content_type="application/json")

