# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
import logging, time

logger = logging.getLogger('card')

class ExamResults(models.Model):
    result_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50L, blank=True)
    ext1 = models.TextField(blank=True)
    ext2 = models.TextField(blank=True)
    ext3 = models.TextField(blank=True)
    ext4 = models.TextField(blank=True)
    ext5 = models.TextField(blank=True)
    ext6 = models.TextField(blank=True)
    ext7 = models.TextField(blank=True)
    def __unicode__(self):
        return self.name;
    class Meta:
        db_table = 'exam_results'

class School(models.Model):
    school_id = models.IntegerField(primary_key=True)
    school_name = models.CharField(max_length=100L, blank=True)
    area = models.CharField(max_length=100L, blank=True)
    school_icon = models.CharField(max_length=1000L, blank=True)
    school_type = models.CharField(max_length=100L, blank=True)
    school_category = models.CharField(max_length=100L, blank=True)
    school_property1 = models.CharField(max_length=100L, blank=True)
    school_property2 = models.CharField(max_length=100L, blank=True)
    school_url = models.CharField(max_length=100L, blank=True)
    school_detail = models.TextField(blank=True)
    school_cost = models.TextField(blank=True)
    def __unicode__(self):
        return self.school_name;
    class Meta:
        db_table = 'school'

class SchoolPoint(models.Model):
    point_id = models.IntegerField(primary_key=True)
    school_id = models.IntegerField()
    school_name = models.CharField(max_length=100L, blank=True)
    specialty_category = models.CharField(max_length=100L, blank=True)
    area = models.CharField(max_length=100L, blank=True)
    type = models.CharField(max_length=100L, blank=True)
    year = models.CharField(max_length=100L, blank=True)
    point_average = models.CharField(max_length=100L, blank=True)
    point_height = models.CharField(max_length=100L, blank=True)
    point_low = models.CharField(max_length=100L, blank=True)
    level = models.CharField(max_length=100L, blank=True)
    class Meta:
        db_table = 'school_point'

class SchoolSpecialtyRelations(models.Model):
    relation_id = models.IntegerField(primary_key=True)
    school_name = models.CharField(max_length=100L)
    specialty_name = models.CharField(max_length=100L)
    specialty_category = models.CharField(max_length=100L, blank=True)
    school_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'school_specialty_relations'

class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    lft = models.IntegerField()
    rgt = models.IntegerField()
    parent_id = models.IntegerField()
    create_time = models.DateTimeField(null=True, blank=True)
    is_deleted = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200L)
    url = models.CharField(max_length=200L, blank=True)
    notes = models.TextField(blank=True)
    def __unicode__(self):
        return self.title;
    class Meta:
        db_table = 'categories'

class Contents(models.Model):
    content_id = models.AutoField(primary_key=True)
    content_category_id = models.IntegerField(null=True, blank=True)
    order_num = models.IntegerField(null=True, blank=True)
    content_type = models.IntegerField(null=True, blank=True)
    is_deleted = models.IntegerField()
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    layout = models.CharField(max_length=100L, blank=True)
    subject = models.CharField(max_length=200L)
    link_to = models.CharField(max_length=200L, blank=True)
    summary = models.CharField(max_length=200L, blank=True)
    content = models.TextField(blank=True)
    image = models.CharField(max_length=255L, blank=True)
    def __unicode__(self):
        return self.subject
    class Meta:
        db_table = 'contents'

class Results(models.Model):
    rid = models.AutoField(primary_key=True) # Field renamed because it started with '_'.
    e = models.IntegerField(null=True, blank=True)
    i = models.IntegerField(null=True, blank=True)
    s = models.IntegerField(null=True, blank=True)
    n = models.IntegerField(null=True, blank=True)
    t = models.IntegerField(null=True, blank=True)
    f = models.IntegerField(null=True, blank=True)
    j = models.IntegerField(null=True, blank=True)
    p = models.IntegerField(null=True, blank=True)
    createtime = models.DateTimeField(null=True, blank=True)
    updatetime = models.DateTimeField(null=True, blank=True)
    def __unicode__(self):
        return self.createtime.strftime('%b-%d-%y %H:%M:%S');
    class Meta:
        db_table = 'results'

class Mbti(models.Model):
    mbti_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50L, blank=True)
    value = models.CharField(max_length=50L, blank=True)
    ext1 = models.TextField(blank=True)
    ext2 = models.TextField(blank=True)
    ext3 = models.TextField(blank=True)
    ext4 = models.TextField(blank=True)
    ext5 = models.TextField(blank=True)
    ext6 = models.TextField(blank=True)
    ext7 = models.TextField(blank=True)
    createtime = models.DateTimeField(null=True, blank=True)
    updatetime = models.DateTimeField(null=True, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'mbti'

class MbtiProfessions(models.Model):
    mbti_pro_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50L, blank=True)
    createtime = models.DateTimeField(null=True, blank=True)
    updatetime = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'mbti_professions'

class MbtiProfessionRelation(models.Model):
    mbti_pro_rel_id = models.AutoField(primary_key=True)
    mbti_id = models.ForeignKey(Mbti)
    mbti_pro_id = models.ForeignKey(MbtiProfessions)
    class Meta:
        db_table = 'mbti_profession_relation'

class MbtiProfessionSpecialty(models.Model):
    mbti_pro_rel_id = models.AutoField(primary_key=True)
    mbti_id = models.IntegerField()
    mbti_pro_id = models.IntegerField()
    mbti_spe_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'mbti_profession_specialty'

class MbtiSpecialty(models.Model):
    mbti_spe_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50L, blank=True)
    createtime = models.DateTimeField(null=True, blank=True)
    updatetime = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'mbti_specialty'

class MbtiSpecialtyPart(models.Model):
    spe_id = models.AutoField(primary_key=True)
    part = models.CharField(max_length=255L, blank=True)
    name = models.CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'mbti_specialty_part'

class Pageviewlogs(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(null=True, blank=True)
    logtime = models.DateTimeField()
    user_agent = models.CharField(max_length=512L, blank=True)
    domain = models.CharField(max_length=255L, blank=True)
    uri = models.CharField(max_length=2048L)
    ext1 = models.CharField(max_length=1000L, blank=True)
    ext2 = models.CharField(max_length=1000L, blank=True)
    ext3 = models.CharField(max_length=1000L, blank=True)
    referer = models.CharField(max_length=2048L, blank=True)
    ip = models.CharField(max_length=100L, blank=True)
    sessionid = models.CharField(max_length=100L, blank=True)
    def __unicode__(self):
        return self.uri
    class Meta:
        db_table = 'pageviewlogs'