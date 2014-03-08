from django.shortcuts import render, render_to_response
from django.template import RequestContext

# Create your views here.
def scrmgr(request):
	return render_to_response("scrmgr/index.html", context_instance=RequestContext(request, {'request':request}))

