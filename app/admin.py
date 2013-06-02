#-*- coding: UTF-8 -*-
from app.models import *
# from django.contrib import admin
import xadmin

xadmin.site.register(School)
xadmin.site.register(ExamResults)
xadmin.site.register(Categories)
xadmin.site.register(Contents)
xadmin.site.register(Results)