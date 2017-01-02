from django.shortcuts import render_to_response
from django.template.context import RequestContext


def technical(request):
    return render_to_response('technical.html', context_instance=RequestContext(request))
