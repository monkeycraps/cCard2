#-*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.core.context_processors import request
from django.utils import simplejson
from django.conf import settings
from app.models import Results, Mbti, MbtiProfessionRelation, MbtiProfessions, Pageviewlogs, User, SchoolPoint, School
from django.db import connection, transaction
from django.http import Http404
from datetime import datetime
from djangosphinx.models import SphinxSearch, SphinxQuerySet

import binascii
import logging
import re
logger = logging.getLogger( 'card' );

# class MyModel(models.Model):
#     search = SphinxSearch() # optional: defaults to db_table
#     # If your index name does not match MyModel._meta.db_table
#     # Note: You can only generate automatic configurations from the ./manage.py script
#     # if your index name matches.
#     search = SphinxSearch('index_name')

#     # Or maybe we want to be more.. specific
#     searchdelta = SphinxSearch(
#         index='index_name delta_name',
#         weights={
#             'name': 100,
#             'description': 10,
#             'tags': 80,
#         },
#         mode='SPH_MATCH_ALL',
#         rankmode='SPH_RANK_NONE',
#     )

# queryset = MyModel.search.query('query')
# results1 = queryset.order_by('@weight', '@id', 'my_attribute')
# results2 = queryset.filter(my_attribute=5)
# results3 = queryset.filter(my_other_attribute=[5, 3,4])
# results4 = queryset.exclude(my_attribute=5)[0:10]
# results5 = queryset.count()

# # as of 2.0 you can now access an attribute to get the weight and similar arguments
# for result in results1:
#     print result, result._sphinx
# # you can also access a similar set of meta data on the queryset itself (once it's been sliced or executed in any way)
# print results1._sphinx

def createUser(request):

	get = request.REQUEST;

	if not (get.has_key('stu_type') and get.has_key('from_prov') and get.has_key('mark_cate') ):
		raise Http404

	mobile = ''
	if not get.has_key( 'mobile' ):
		mobile = ''
	else:
		mobile = get.get('mobile')

	u = User( name = mobile, mobile = mobile, stu_type = get.get('stu_type'), createtime= datetime.now(), updatetime =datetime.now(), 
		from_prov = get.get('from_prov'), mark_cate = get.get('mark_cate')
	)
	u.save();

	return HttpResponse( json( {'error': 0, 'uid': u.uid } ) );

def submitResult(request):

	get = request.REQUEST;
	
	if not (get.get('uid'), get.get('e') and get.get('s') and get.get('t') and get.get('j') ):
		raise Http404
	e = int( get.get('e') )
	s = int( get.get('s') )
	t = int( get.get('t') )
	j = int( get.get('j') )
	uid = int( get.get('uid') )

	if not User.objects.get( uid = uid ):
		raise Http404

	mbti_name = 'e' if (e > 50) else 'i'
	mbti_name += 's' if (e > 50) else 'n'
	mbti_name += 't' if (e > 50) else 'f'
	mbti_name += 'j' if (e > 50) else 'p'

	r = Results( e=e, i=100-e, s=s, n=100-s, t=t, 
		f=100-t, j=j, p=100-j, createtime=datetime.now(), updatetime=datetime.now(), uid=uid, mbti = mbti_name )
	r.save()
	# render_404_error();
	# 返回rid 职业列表 
	profession_list = []
	# mbti = Mbti.objects.get( name=mbti_name )
	sql = 'select p.mbti_pro_id, p.name from mbti inner join mbti_profession_relation r on mbti.mbti_id = r.mbti_id inner join mbti_professions p on r.mbti_pro_id = p.mbti_pro_id where mbti.name = \''+ mbti_name +'\' ';
	cursor = connection.cursor()
	cursor.execute( sql )
	rs = dictfetchall( cursor )
	for one in rs: 
		profession_list += [{ 'id':one['mbti_pro_id'],  'name': one['name'] }]

	mbti = Mbti.objects.get( name = mbti_name )
	mbti_info = { 'name': mbti.name, 'summary': mbti.value, 'ext1': mbti.ext1, 'ext2': mbti.ext2, 'ext3': mbti.ext3, 'ext4': mbti.ext4, 'ext5': mbti.ext5, 'ext6': mbti.ext6, 'ext7': mbti.ext7 };

	pvlog(request, r.rid, mbti_name )

	return HttpResponse( json( {'error': 0, 'rid': r.rid, 'mbti': mbti_info, 'profession_list': profession_list } ) );


def getResult(request):

	get = request.REQUEST;
	
	if not (get.get('rid') ):
		raise Http404
	rid = int( get.get('rid') )

	r = Results.objects.get( rid=rid )
	if not r:
		raise Http404

	# render_404_error();
	# 返回rid 职业列表 
	profession_list = []
	# mbti = Mbti.objects.get( name=mbti_name )
	sql = 'select p.mbti_pro_id, p.name from mbti inner join mbti_profession_relation r on mbti.mbti_id = r.mbti_id inner join mbti_professions p on r.mbti_pro_id = p.mbti_pro_id where mbti.mbti_id = \''+ r.mbti +'\' ';
	cursor = connection.cursor()
	cursor.execute( sql )
	rs = dictfetchall( cursor )
	for one in rs: 
		profession_list.append({ 'id': one['mbti_pro_id'] , 'name': one['name'] })

	mbti = Mbti.objects.get( name = r.mbti )
	mbti_info = { 'name': mbti.name, 'summary': mbti.value, 'ext1': mbti.ext1, 'ext2': mbti.ext2, 'ext3': mbti.ext3, 'ext4': mbti.ext4, 'ext5': mbti.ext5, 'ext6': mbti.ext6, 'ext7': mbti.ext7 };

	pvlog(request, r.rid, r.mbti )

	return HttpResponse( json( {'error': 0, 'rid': r.rid, 'mbti': mbti_info, 'profession_list': profession_list } ) );


def mbtiInfo(request): 
	
	get = request.REQUEST;
	
	if not ( get.get('mbti') ):
		raise Http404

	mbti = get.get( 'mbti' )

	mbti = Mbti.objects.get( name = mbti )
	if not mbti:
		raise Http404


	profession_list = []
	# mbti = Mbti.objects.get( name=mbti_name )
	sql = 'select p.mbti_pro_id, p.name from mbti inner join mbti_profession_relation r on mbti.mbti_id = r.mbti_id inner join mbti_professions p on r.mbti_pro_id = p.mbti_pro_id where mbti.name = \''+ mbti.name +'\' ';
	cursor = connection.cursor()
	cursor.execute( sql )
	rs = dictfetchall( cursor )
	for one in rs: 
		profession_list.append({ 'id': one['mbti_pro_id'] , 'name': one['name'] })

	mbti_info = { 'name': mbti.name, 'summary': mbti.value, 'ext1': mbti.ext1, 'ext2': mbti.ext2, 'ext3': mbti.ext3, 'ext4': mbti.ext4, 'ext5': mbti.ext5, 'ext6': mbti.ext6, 'ext7': mbti.ext7 }

	return HttpResponse( json( {'error': 0,  'mbti': mbti_info, 'profession_list': profession_list } ) );


def proInfo(request): 

	get = request.REQUEST;
	
	if not ( get.get('id') ):
		raise Http404

	id = get.get( 'id' )
	pro = MbtiProfessions.objects.get( mbti_pro_id = id )
	if not pro:
		raise Http404;

	return HttpResponse( json({ 'error':0, 'name': pro.name, 'description': pro.description }) );

def filter(request):

	get = request.REQUEST;

	page = get.get( 'page', None )
	if not page:
		page = 1
	else:
		page = int(page)

	limit = 10

	mode = 'SPH_MATCH_ANY';
	# 职业
	pro_id = get.get( 'pro_id', None )
	to_query = ''
	if pro_id:
		spe_list = {}
		# mbti = Mbti.objects.get( name=mbti_name )
		sql = 'select s.mbti_spe_id, s.name from mbti_profession_specialty ps inner join mbti_specialty s on ps.mbti_spe_id = s.mbti_spe_id where ps.mbti_pro_id = '+ pro_id +'';
		cursor = connection.cursor()
		cursor.execute( sql )
		rs = dictfetchall( cursor )
		for one in rs: 
			to_query += ' '+ one['name']
		
	if to_query == "":
		mode = 'SPH_MATCH_FULLSCAN';

	ss = SphinxQuerySet(
        index='ccard', 
        mode=mode,
        rankmode='SPH_RANK_NONE',
        limit=limit,  
        offset= (page - 1) * limit 
    );
	# ss.setm

	from_prov = get.get( 'from_prov', None )
	if from_prov:
		from_prov = from_prov.encode( 'utf-8' )
		from_prov = re.sub( '省$', '', from_pr )
		from_prov = re.sub( '市$', '', from_pr )
		ss = ss.filter( from_prov=mccrc32( from_prov ))

	school_prov = get.get( 'school_prov', None )
	if school_prov:
		school_prov = school_prov.encode( 'utf-8' )
		school_prov = re.sub( '省$', '', school_prov )
		school_prov = re.sub( '市$', '', school_prov )
		ss = ss.filter( school_prov=mccrc32( school_prov ))

	stu_type = get.get( 'stu_type', None )
	if stu_type:
		ss = ss.filter( stu_type=mccrc32( stu_type ))

	level = get.get( 'level', None )
	if level:
		ss = ss.filter( level=mccrc32( level ))

	school_id = get.get( 'school_id', None )
	if school_id:
		ss = ss.filter( school_id=school_id )


	r = ss.query( to_query ).order_by('@weight')
	# for one in r._sphinx:

	rs_list = {}
	ids = []
	i = (page - 1) * limit 
	for one in list(r):
		id = one.get( 'id' )
		i = i+1
		rs_list[i] = str(id)
		ids.append(str(id))

	if len(ids) > 0 :
		sql = 'select s.school_id, s.school_name, s.area as school_prov, s.school_icon, s.school_type, s.school_property1, s.school_property2, s.school_url, mp.point_id, mp.specialty_category, mp.area as from_prov, mp.type as stu_type, mp.year, mp.point_average, mp.point_height, mp.point_low, mp.level from school s inner join school_point mp on s.school_id = mp.school_id where mp.point_id in ( '+ (', '.join(ids)) +' )'
		tmp = {}
		cursor = connection.cursor()
		cursor.execute( sql )
		rs = dictfetchall( cursor )
		for one in rs: 
			tmp[str(one['point_id'])] = ones

		for key, one in rs_list.iteritems():
			rs_list[key] = tmp[one]

		rs_list_out = []
		for key in rs_list:
			rs_list_out.append( rs_list[key] )

	# return HttpResponse( s );

	return HttpResponse( json({ 'error':0, 'page': page, 'limit': limit, 'rs_list': rs_list_out }) );

def school(request):

	get = request.REQUEST;

	id = get.get( 'id', None )
	if not id:
		raise Http404

	s = School.objects.get( school_id=id )

	specialties = []
	withpro = get.get( 'withpro', None )
	if withpro == '1':

		condition_tmp = {}

		from_prov = get.get( 'from_prov', None )
		if from_prov:
			from_prov = from_prov.encode( 'utf-8' )
			from_prov = re.sub( '省$', '', from_prov )
			from_prov = re.sub( '市$', '', from_prov )
			condition_tmp['area'] = from_prov

		stu_type = get.get( 'stu_type', None )
		if stu_type:
			condition_tmp['type'] = stu_type

		condition = ''
		if len( condition_tmp ) > 0 : 
			for key in condition_tmp:
				condition += ' and '+ key + ' = \''+ condition_tmp[key] +'\' '

		sql = 'select point_id id, specialty_category spe_name, area from_prov, type stu_type, year, point_average, point_height, point_low, level from school_point where school_id = '+ id +' and year = 2012 '+ condition
		cursor = connection.cursor()
		cursor.execute( sql )
		specialties = dictfetchall( cursor )

	return HttpResponse( json({ 'error':0, 'name': s.school_name, 'school_detail': s.school_detail, 'school_icon': s.school_icon, 'school_prov': s.area, 'school_type': s.school_type, 'school_category': s.school_category, 'school_property1': s.school_property1, 'school_property2': s.school_property2, 'specialties': specialties }) );

def sFilter(request): 

	get = request.REQUEST;

	page = get.get( 'page', None )
	if not page:
		page = 1
	else:
		page = int(page)

	limit = 10
	offset = (page-1) * limit 

	condition_tmp = {}
	school_prov = get.get( 'school_prov', None )
	if school_prov:
		school_prov = school_prov.encode( 'utf-8' )
		school_prov = re.sub( '省$', '', school_prov )
		school_prov = re.sub( '市$', '', school_prov )
		condition_tmp['s.area'] = school_prov

	from_prov = get.get( 'from_prov', None )
	if from_prov:
		from_prov = from_prov.encode( 'utf-8' )
		from_prov = re.sub( '省$', '', from_prov )
		from_prov = re.sub( '市$', '', from_prov )
		condition_tmp['sp.area'] = from_prov

	stu_type = get.get( 'stu_type', None )
	if stu_type:
		condition_tmp['sp.type'] = stu_type

	level = get.get( 'level', None )
	if level:
		condition_tmp['level'] = level

	name = get.get( 'name', None )
	if name:
		condition_tmp['s.school_name'] = name

	condition = ' where sp.year = 2012 ';
	params = []
	if len(condition_tmp) > 0:
		for key in condition_tmp:
			if key == 's.school_name':
				condition += ' and ' + key + ' like ( %s ) '
				params.append( '%'+ condition_tmp[key] + '%' )
			else:
				condition += ' and ' + key + ' = \''+ condition_tmp[key] +'\' '
		condition = re.sub( 'and $', '', condition )

	sql = 'SELECT s.school_id, s.school_name, s.school_icon FROM school s INNER JOIN school_point sp ON s.school_id = sp.school_id '+ condition + " GROUP BY s.school_id limit "+ str(limit) + ' offset '+ str(offset);
	# logger.info( sql )

	cursor = connection.cursor()
	cursor.execute( sql, params )
	list = dictfetchall( cursor )

	return HttpResponse( json({ 'error': 0, 'list': list }) )

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

def mccrc32( szString ):
    return binascii.crc32(szString)& 0xffffffff