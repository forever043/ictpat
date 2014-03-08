# coding=utf-8
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db import IntegrityError, DatabaseError

# Create your views here.
def patretvmgr(request):
	return render_to_response("patmgr/patretvmgr.html", context_instance=RequestContext(request, {'request':request}))


