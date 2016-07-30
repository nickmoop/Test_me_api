from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader, Context
from django.middleware import csrf
from django.conf import settings
import json

from test_me_api.models import Text

my_ip_address = '10.10.2.10'
host_name = 'http://' + my_ip_address + '/test_me_api/'

def index(request):
    global host_name
    return redirect(host_name + 'uploadTextPage/')

def apiProcessor(request, api_command):
    global host_name

    if request.method == 'GET' and request.is_ajax():
        if api_command == 'uploadText':
            uploaded_text = request.GET.get('text', '')
            text = Text(body = uploaded_text)
            text.save()
            message = 'you wonna send ' + str(uploaded_text)
            return(JsonResponse({'error_message' : message, 'redirect_url' : host_name + 'api/getText'}))

    if api_command == 'getText':
        all_text_entries = Text.objects.all()
        template = loader.get_template('test_me_api/showText.html')
        context = RequestContext(request, {'all_text_entries' : all_text_entries})
        return HttpResponse(template.render(context))

    template = loader.get_template('test_me_api/showApiCommand.html')
    context = RequestContext(request, {'api_command' : str(api_command)})
    return HttpResponse(template.render(context))

def uploadTextPage(request):
    global host_name

    api_link = host_name + 'api/uploadText'
    template = loader.get_template('test_me_api/uploadText.html')
    context = RequestContext(request, {'api_link' : api_link})
    return HttpResponse(template.render(context))

def admin(request):
    global host_name

    if request.method == 'POST' and request.is_ajax():
        text_pk_to_delete = request.POST.get('text_pk', '')
        text_to_delete = Text.objects.get(pk = text_pk_to_delete).body
        message = 'you wonna delete : pk = ' + str(text_pk_to_delete) + ' text = ' + str(text_to_delete)
        Text.objects.filter(pk = text_pk_to_delete).delete()
        return(JsonResponse({'error_message' : message, 'redirect_url' : host_name + 'admin'}))

    all_text_entries = Text.objects.all()
    template = loader.get_template('test_me_api/admin.html')
    context = RequestContext(request, {'all_text_entries' : all_text_entries})
    return HttpResponse(template.render(context))
