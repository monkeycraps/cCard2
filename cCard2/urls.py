#-*- coding: UTF-8 -*-
import xadmin
xadmin.autodiscover()

from django.conf.urls import patterns, include, url

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.registe_models()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
#     url(r'^cCard2/', include('cCard2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
#     url(r'^admin/', include(admin.site.urls)),
    url(r'xadmin/', include(xadmin.site.urls)),
    # url(r'api/', 'api.views', name='api'),
)

urlpatterns += patterns('api.views', 
	url(r'^api/submitResult', 'submitResult'), 
	url(r'^api/mbtiinfo', 'mbtiinfo'), 
)