# coding=utf-8
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db import IntegrityError, DatabaseError
from django.core import exceptions

from patmgr.models import Department
from patmgr.models import Patent


def patdetail(request, patent_id):

	#patent = get_object_or_404(Patent, id=patent_id)

	error_msg = ""
	try:
		patent = Patent.objects.get(id=patent_id)
	except DoesNotExist, x:
		error_msg = x.__unicode__()

	return render_to_response("patmgr/patlist.html",
				  { 'patent' : patent,
				    'error_msg' : error_msg },
				  context_instance=RequestContext(request, {'request':request}))

