#-*- coding: UTF-8 -*-
import sys 
import settings 
from django.core.management import setup_environ 
sys.path.append(settings.PROJECT_PATH) 
setup_environ(settings) 
from django.db import connection, transaction

import logging
logger = logging.getLogger( 'card' );

i = 0;

reload(sys)
sys.setdefaultencoding('utf-8')

print sys.getdefaultencoding()

def dictfetchall(cursor):
    # "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
	    dict(zip([col[0] for col in desc], row))
	    for row in cursor.fetchall()
    ]	

args = sys.argv
act = ''
if len(args) > 1:
	act = args[1]

if 'update-point' == act:
	print 'update point'

	i = 0;

	while( True ):

		sql = 'select * from school_point order by point_id limit '+ str(i) + ', 1000';

		cursor = connection.cursor()
		cursor.execute( sql )
		rs = dictfetchall( cursor )

		if not rs: 
			break;

		for one in rs: 
			# 加入school_point3
			sql = 'select * from school_point2 where school_id = ' + str(one['school_id']) + ' and \
				specialty_category = \'' + str(one['specialty_category'])+ '\' and \
				area = \'' + str(one['area'])+ '\' and type = \'' + str(one['type'])+ '\' \
				and year < ' + str(one['year']);
			cursor.execute( sql )
			rs1 = dictfetchall( cursor );
			if rs1:
				# 删除
				for one1 in rs1:
					sql = 'delete from school_point2 where point_id = '+ str(one1['point_id'])
					cursor.execute( sql )

			sql = 'insert into school_point2 ( point_id, school_id, school_name, specialty_category, area, type, year, point_average, point_height, point_low, level ) values ( '+ str(one['point_id']) +', '+ str(one['school_id']) +', \''+ str(one['school_name']) +'\', \''+ str(one['specialty_category']) +'\', \''+ str(one['area']) +'\', \''+ str(one['type']) +'\', \''+ str(one['year']) +'\', \''+ str(one['point_average']) +'\', \''+ str(one['point_height']) +'\', \''+ str(one['point_low']) +'\', \''+ str(one['level']) +'\' )' 
			cursor.execute( sql )

		i = i + 1000
		print i
		# break;
	
	return HttpResponse( json( {'error': 0, 'uid': 0 } ) );

if 'fix-spe' == act:
	print 'fixspe start'

	i = 0;

	while( True ):

		sql = 'select * from school_point3 where relation_id = 0 order by point_id limit '+ str(i) + ', 1000';

		cursor = connection.cursor()
		cursor.execute( sql )
		rs = dictfetchall( cursor )

		if not rs: 
			break;

		for one in rs: 
			# 查找 relation_id
			relation_id = 0;
			sql = 'select relation_id from school_specialty_relations where school_id = ' + str(one['school_id']) \
				+ ' and specialty_name = \'' + str(one['specialty_category']) + '\''
			# print sql
			# break;
			cursor.execute( sql )
			rs1 = dictfetchall( cursor )
			for one1 in rs1:
				relation_id = one1['relation_id']
				break

			sql = 'update school_point3 set relation_id = ' + str( relation_id ) + ' where point_id = '+ str( one['point_id'] )
			# print sql
			cursor.execute( sql )

		i = i + 1000
		print i
		# break;


if 'fix-relation' == act:
	print 'fix relation start'

	i = 0;
	size = 1000

	while( True ):

		sql = 'select * from school_point3 where relation_id = 0 order by point_id limit '+ str(i) + ', '+ str(size);

		cursor = connection.cursor()
		cursor.execute( sql )
		rs = dictfetchall( cursor )

		if not rs: 
			break;

		for one in rs: 

			sql = 'select * from school_specialty_relations where school_id = '+ str(one['school_id']) +' and specialty_name = \''+ one['specialty_category'] +'\'';

			cursor = connection.cursor()
			cursor.execute( sql )
			rs1 = dictfetchall( cursor )

			if rs1: 
				continue;

			# 加入relation 
			sql = 'insert into school_specialty_relations (school_name, specialty_name, specialty_category, school_id) \
				values( \''+ one['school_name'] +'\', \''+ one['specialty_category'] +'\', \'\', '+ str(one['school_id']) +' )'
			# print sql
			cursor.execute( sql )

		i = i + size
		print i
		# break;



if 'fix-relation1' == act:
	print 'fix relation1 start'

	i = 0;
	size = 1000

	while( True ):

		sql = 'select * from school_point3 order by point_id limit '+ str(i) + ', '+ str(size);

		cursor = connection.cursor()
		cursor.execute( sql )
		rs = dictfetchall( cursor )

		if not rs: 
			break;

		for one in rs: 
			print one

			# 加入level 
			sql = 'update school_specialty_relations set level = \''+ one['level'] +'\' where relation_id = '+ str( one['relation_id'] )
			# print sql
			cursor.execute( sql )

		i = i + size
		print i
		# break;


