# coding=utf-8
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db import IntegrityError, DatabaseError
from django.core import exceptions

from patmgr.models import Patent
from patmgr.models import Department

from patmgr.forms import PatentFormBasic
from patmgr.forms import PatentFormAdvance


#def patlist(request):
#	deplist = Department.objects.all()
#	patlist = Patent.objects.all()
#	return render_to_response("patmgr/patlist.html",
#				  { 'department_list' : deplist, 'patent_list' : patlist},
#				  context_instance=RequestContext(request, {'request':request}))



def patdelete(request, patent_id):

	success_msg = ""
	error_msg = ""

	try:
		patent = Patent.objects.get(id=patent_id)
		patent.delete()
	except DoesNotExist:
		error_msg = ""
	except IntegrityError, x:
		error_msg = u"数据约束错误: " + x.__unicode__()
	except DatabaseError, x:
		error_msg = u"数据库错误: " + x.__unicode__()
	except:
		error_msg = u"未知错误"

	if not error_msg:
		success_msg = u"删除成功"

	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

	#return render_to_response("patmgr/patlist.html",
	#			  { 'department_list' : deplist,
	#			    'patent_list' : patlist,
	#			    'error_msg' : error_msg,
	#			    'success_msg' : success_msg},
	#			  context_instance=RequestContext(request, {'request':request}))


def patedit(request, patent_id):

	# retrieve data from DB
	patent = get_object_or_404(Patent, id=patent_id)

	# Not POST, show form data
	if request.method != 'POST':

		formBsc = PatentFormBasic({ 'name'       : patent.name,
					    'department' : patent.department,
					    'inventors'  : patent.inventors,
					    'type'       : patent.type,
					    'state'      : patent.state,
					    'apply_code' : patent.apply_code,
					    'apply_date' : patent.apply_date,
					    'authorize_code' : patent.authorize_code,
					    'authorize_date' : patent.authorize_date })

		return render_to_response("patmgr/patedit.html",
					  { 'extmode': False,
					    'patent_id': patent_id,
					    'formBsc': formBsc,
					    'formAdv': PatentFormAdvance() },
					  context_instance=RequestContext(request, {'request':request}))

	# POST data, update DB
	else:

		formBsc = PatentFormBasic(request.POST)
		if formBsc.is_valid():
			cd = formBsc.cleaned_data
			patent.name = cd['name']
			patent.department = cd['department']
			patent.inventors = cd['inventors']
			patent.type = cd['type']
			patent.state = cd['state']
			patent.apply_code = cd['apply_code']
			patent.apply_date = cd['apply_date']
			patent.authorize_code = cd['authorize_code']
			patent.authorize_date = cd['authorize_date']

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
				success_msg = u"专利\"" + patent.name + u"\"信息更新成功"
			else:
				success_msg = ""
			
			return render_to_response("patmgr/patedit.html",
					          { 'extmode': False,
					    	    'patent_id': patent_id,
						    'formBsc': formBsc,
						    'formAdv': PatentFormAdvance(),
						    'error_msg': error_msg,
						    'success_msg': success_msg },
						  context_instance=RequestContext(request, {'request':request}))
		else:
			return render_to_response("patmgr/patedit.html",
					          { 'extmode': False,
						    'patent_id': patent_id,
						    'formBsc': formBsc,
						    'formAdv': PatentFormAdvance(),
						    'error_msg': '信息更新失败'},
						  context_instance=RequestContext(request, {'request':request}))


def pateditext(request, patent_id):
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


