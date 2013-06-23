#-*- coding: UTF-8 -*-
from app.models import *
# from django.contrib import admin
import xadmin

xadmin.site.register(User)
xadmin.site.register(Results)
xadmin.site.register(Pageviewlogs)
xadmin.site.register(School)
xadmin.site.register(Mbti)
xadmin.site.register(Categories)
xadmin.site.register(Contents)
xadmin.site.register(MbtiProfessions)
xadmin.site.register(MbtiProfessionRelation)
xadmin.site.register(MbtiSpecialty)
