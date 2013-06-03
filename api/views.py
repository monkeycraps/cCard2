#-*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.core.context_processors import request
from django.utils import simplejson
from django.conf import settings
from app.models import Results, Mbti, MbtiProfessionRelation, MbtiProfessions, Pageviewlogs
from django.db import connection, transaction
from django.http import Http404
from datetime import datetime

import logging
logger = logging.getLogger( 'card' );

def submitResult(request):

	get = request.REQUEST;
	logger.info( get )
	
	if not (get.get('e') and get.get('s') and get.get('t') and get.get('j') ):
		raise Http404
	e = int( get.get('e') )
	s = int( get.get('s') )
	t = int( get.get('t') )
	j = int( get.get('j') )

	mbti_name = 'e' if (e > 50) else 'i'
	mbti_name += 's' if (e > 50) else 'n'
	mbti_name += 't' if (e > 50) else 'f'
	mbti_name += 'j' if (e > 50) else 'p'

	r = Results( e=e, i=100-e, s=s, n=100-s, t=t, 
		f=100-t, j=j, p=100-j, createtime=datetime.now(), updatetime=datetime.now() )
	r.save()
	# render_404_error();
	# 返回rid 职业列表 
	profession_list = {}
	# mbti = Mbti.objects.get( name=mbti_name )
	sql = 'select p.mbti_pro_id, p.name from mbti inner join mbti_profession_relation r on mbti.mbti_id = r.mbti_id inner join mbti_professions p on r.mbti_pro_id = p.mbti_pro_id where mbti.name = \''+ mbti_name +'\' ';
	cursor = connection.cursor()
	cursor.execute( sql )
	rs = dictfetchall( cursor )
	# logger.info( rs )
	for one in rs: 
		logger.info( one )
		profession_list[one['mbti_pro_id']] = { 'name': one['name'] }

	pvlog(request, r.rid, mbti_name )

	return HttpResponse( json( {'error': 0, 'rid': r.rid, 'profession_list': profession_list } ) );

def mbtiinfo(request): 
	
	get = request.REQUEST;
	
	if not ( get.get('mbti') ):
		raise Http404

	mbti = get.get( 'mbti' )
	rid = get.get( 'rid' )
	pro_id = get.get( 'pro_id' )

	r = Mbti.objects.get( name = mbti )
	if not r:
		raise Http404

	pvlog( request, rid, id, pro_id )

	return HttpResponse( json( {'error': 0, 'ext1': r.ext1, 'ext2': r.ext2, 'ext3': r.ext3, 'ext4': r.ext4, 'ext5': r.ext5, 'ext6': r.ext6, 'ext7': r.ext7 } ) );



def json(data):
	encode = settings.DEFAULT_CHARSET
	return HttpResponse(simplejson.dumps(uni_str(data, encode)))

def uni_str(a, encoding):
	if isinstance(a, (list, tuple)):
		s = []
		for i, k in enumerate(a):
			s.append(uni_str(k, encoding))
		return s
	elif isinstance(a, dict):
		s = {}
		for i, k in enumerate(a.items()):
			key, value = k
			s[uni_str(key, encoding)] = uni_str(value, encoding)
		return s
	elif isinstance(a, str) or (hasattr(a, '__str__') and callable(getattr(a, '__str__'))):
		if getattr(a, '__str__'):
			a = str(a)
		return unicode(a, encoding)
	elif isinstance(a, unicode):
		return a
	else:
		return a


def dictfetchall(cursor):
    # "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
	    dict(zip([col[0] for col in desc], row))
	    for row in cursor.fetchall()
    ]

def pvlog( request, id, ext1 = None, ext2 = None, ext3 = None ):

	uri = request.META['PATH_INFO']
	user_agent = request.META['HTTP_USER_AGENT']
	ip = request.META['REMOTE_ADDR']
	pv = Pageviewlogs(uid=id, ext1=ext1, ext2=ext2, ext3=ext3, user_agent=user_agent, uri=uri, ip=ip)
	pv.save()
