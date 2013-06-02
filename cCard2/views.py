#-*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.core.context_processors import request

def home(request):
    return new HttpResponse( "hey 志愿卡" );