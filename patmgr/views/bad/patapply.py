# coding=utf-8
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db import IntegrityError, DatabaseError

from patmgr.models import Patent

from patmgr.forms import PatentFormBasic
from patmgr.forms import PatentFormAdvance


def patapply(request):
	return render_to_response("patmgr/patapply.html",
				  { 'basic_mode': True,
				    'formBsc': PatentFormBasic(),
				    'formAdv': PatentFormAdvance() },
				  context_instance=RequestContext(request, {'request':request}))

def patapply_basic(request):
	if request.method != 'POST':
		return HttpResponseRedirect('/dashboard/pat/apply/')

	formBsc = PatentFormBasic(request.POST, request.FILES)
	if formBsc.is_valid():
		cd = formBsc.cleaned_data
		patent = Patent(name = cd['name'],
				department = cd['department'],
				inventors = cd['inventors'],
				type = cd['type'],
				state = cd['state'],
				apply_code = cd['apply_code'],
				apply_date = cd['apply_date'],
				authorize_code = cd['authorize_code'],
				authorize_date = cd['authorize_date'])

		error_msg = ""
		try:
			patent.save();
		except IntegrityError, x:
			error_msg = u"数据约束错误: " + x.__unicode__()
		except DatabaseError, x:
			error_msg = u"数据库错误: " + x.__unicode__()
		except:
			error_msg = u"未知错误"

		if not error_msg:
			success_msg = u"专利\"" + patent.name + u"\"添加成功"
			formBsc = PatentFormBasic()
		else:
			success_msg = ""
			
		return render_to_response("patmgr/patapply.html",
				          { 'basic_mode': True,
					    'formBsc': formBsc,
					    'formAdv': PatentFormAdvance(),
					    'error_msg': error_msg,
					    'success_msg': success_msg },
					  context_instance=RequestContext(request, {'request':request}))
	else:
		return render_to_response("patmgr/patapply.html",
				          { 'basic_mode': True,
					    'formBsc': formBsc,
					    'formAdv': PatentFormAdvance(),
					    'error_msg': u'添加失败'},
					  context_instance=RequestContext(request, {'request':request}))


def patapply_advance(request):
	if request.method != 'POST':
		return HttpResponseRedirect('/dashboard/pat/apply/')
	
	formAdv = PatentFormAdvance(request.POST)
	if formAdv.is_valid():
		cd = formAdv.cleaned_data

		return render_to_response("patmgr/patapply.html",
				          { 'advance_mode': True,
					    'formBsc': PatentFormBasic(),
					    'formAdv': PatentFormAdvance(),
					    'success_msg': '添加成功'},
					  context_instance=RequestContext(request, {'request':request}))
	else:
		return render_to_response("patmgr/patapply.html",
				          { 'advance_mode': True,
					    'formBsc': PatentFormBasic(),
					    'formAdv': formAdv,
					    'error_msg': '添加失败'},
					  context_instance=RequestContext(request, {'request':request}))


