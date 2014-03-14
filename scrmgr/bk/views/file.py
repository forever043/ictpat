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

from scrmgr.models import Software

class SCRFileView(View):
	def get(self, request, *args, **kwargs):
		file = None
		fcode = kwargs["fcode"]
		match_scr = Software.objects.filter(Q(apply_code=fcode)|Q(authorize_code=fcode))
		if match_scr and len(match_scr)==1:
			scr = match_scr[0]
			if fcode == scr.apply_code:
				file = scr.apply_file
			elif fcode == scr.authorize_code:
				file = scr.authorize_file
		return serve_file(request, file, save_as=False)

class SCRFileUploadView(View):
	def get(self, request, *args, **kwargs):
		return HttpResponse('')

	def post(self, request, *args, **kwargs):
		files = []
		for field, file in request.FILES.iteritems():
			file_entry = {"name": file.name, "size": file.size}

			filename, ext = os.path.splitext(file.name)
			match_scr = Software.objects.filter(Q(apply_code=filename)|Q(authorize_code=filename))
			if not match_scr:
				file_entry["error"] = "无对应软件"
			elif len(match_scr) > 1:
				file_entry["error"] = "软件数据库中申请号或授权号不唯一：%s" % filename
			else:
				scr = match_scr[0]
				if scr.apply_code == filename:
					scr.apply_file = file
					file_entry["name"] = u"申请文件：%s" % scr.name
					file_entry["url"] = reverse("scr-file-service", args=(scr.apply_code,))
				else:
					scr.authorize_file = file
					file_entry["name"] = u"授权文件：%s" % scr.name
					file_entry["url"] = reverse("scr-file-service", args=(scr.authorize_code,))
				scr.save()
				file_entry["thumbnailUrl"] = "/resources/images/icon_pdf.png"
				file_entry["deleteUrl"] = file_entry["url"]
				file_entry["deleteType"] = "DELETE"
			files.append(file_entry);

		return HttpResponse(json.dumps({"files": files}), content_type="application/json")


