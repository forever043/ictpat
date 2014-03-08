# coding=utf-8
import os
from django.http import HttpResponse
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

class PatentFileView(View):
	def get(self, request, *args, **kwargs):
		file = None
		fcode = kwargs["fcode"]
		match_patent = Patent.objects.filter(Q(apply_code=fcode)|Q(authorize_code=fcode))
		if match_patent and len(match_patent)==1:
			patent = match_patent[0]
			if fcode == patent.apply_code:
				file = patent.apply_file
			elif fcode == patent.authorize_code:
				file = patent.authorize_file
		return serve_file(request, file, save_as=False)

class PatentFileUploadView(View):
	def get(self, request, *args, **kwargs):
		return HttpResponse('')

	def post(self, request, *args, **kwargs):
		files = []
		for field, file in request.FILES.iteritems():
			file_entry = {"name": file.name, "size": file.size}

			filename, ext = os.path.splitext(file.name)
			match_patent = Patent.objects.filter(Q(apply_code=filename)|Q(authorize_code=filename))
			if not match_patent:
				file_entry["error"] = "无对应专利"
			elif len(match_patent) > 1:
				file_entry["error"] = "专利数据库中申请号或授权号不唯一：%s" % filename
			else:
				patent = match_patent[0]
				if patent.apply_code == filename:
					patent.apply_file = file
					file_entry["name"] = u"申请文件：%s" % patent.name
					file_entry["url"] = reverse("patent-file-service", args=(patent.apply_code,))
				else:
					patent.authorize_file = file
					file_entry["name"] = u"授权文件：%s" % patent.name
					file_entry["url"] = reverse("patent-file-service", args=(patent.authorize_code,))
				patent.save()
				file_entry["thumbnailUrl"] = "/resources/images/icon_pdf.png"
				file_entry["deleteUrl"] = file_entry["url"]
				file_entry["deleteType"] = "DELETE"
			files.append(file_entry);

		return HttpResponse(json.dumps({"files": files}), content_type="application/json")


