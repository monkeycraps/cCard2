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

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80L, unique=True)
    class Meta:
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group_id = models.IntegerField()
    permission_id = models.IntegerField()
    class Meta:
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100L)
    class Meta:
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128L)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(max_length=30L, unique=True)
    first_name = models.CharField(max_length=30L)
    last_name = models.CharField(max_length=30L)
    email = models.CharField(max_length=75L)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    group_id = models.IntegerField()
    class Meta:
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    permission_id = models.IntegerField()
    class Meta:
        db_table = 'auth_user_user_permissions'

class Categories(models.Model):
    category_id = models.IntegerField(primary_key=True)
    lft = models.IntegerField()
    rgt = models.IntegerField()
    parent_id = models.IntegerField()
    create_time = models.DateTimeField(null=True, blank=True)
    is_deleted = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200L)
    url = models.CharField(max_length=200L, blank=True)
    notes = models.TextField(blank=True)
    class Meta:
        db_table = 'categories'

class Contents(models.Model):
    content_id = models.IntegerField(primary_key=True)
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
    class Meta:
        db_table = 'contents'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100L)
    app_label = models.CharField(max_length=100L)
    model = models.CharField(max_length=100L)
    class Meta:
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40L, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100L)
    name = models.CharField(max_length=50L)
    class Meta:
        db_table = 'django_site'

class ExamResults(models.Model):
    result_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L, blank=True)
    ext1 = models.TextField(blank=True)
    ext2 = models.TextField(blank=True)
    ext3 = models.TextField(blank=True)
    ext4 = models.TextField(blank=True)
    ext5 = models.TextField(blank=True)
    ext6 = models.TextField(blank=True)
    ext7 = models.TextField(blank=True)
    class Meta:
        db_table = 'exam_results'

class Exams(models.Model):
    field_id = models.IntegerField(primary_key=True, db_column='_id') # Field renamed because it started with '_'.
    type = models.TextField(blank=True)
    title = models.TextField(blank=True)
    ans_a = models.TextField(blank=True)
    ans_b = models.TextField(blank=True)
    type_a = models.TextField(blank=True)
    type_b = models.TextField(blank=True)
    imgurl = models.TextField(blank=True)
    class Meta:
        db_table = 'exams'

class Mbti(models.Model):
    mbti_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L, blank=True)
    value = models.CharField(max_length=50L, blank=True)
    createtime = models.DateTimeField(null=True, blank=True)
    updatetime = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'mbti'

class MbtiProfessionRelation(models.Model):
    mbti_pro_rel_id = models.IntegerField(primary_key=True)
    mbti_id = models.ForeignKey()
    mbti_pro_id = models.IntegerField()
    class Meta:
        db_table = 'mbti_profession_relation'

class MbtiProfessionSpecialty(models.Model):
    mbti_pro_rel_id = models.IntegerField(primary_key=True)
    mbti_id = models.IntegerField()
    mbti_pro_id = models.IntegerField()
    mbti_spe_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'mbti_profession_specialty'

class MbtiProfessions(models.Model):
    mbti_pro_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L, blank=True)
    createtime = models.DateTimeField(null=True, blank=True)
    updatetime = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'mbti_professions'

class MbtiSpecialty(models.Model):
    mbti_spe_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L, blank=True)
    createtime = models.DateTimeField(null=True, blank=True)
    updatetime = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'mbti_specialty'

class MbtiSpecialtyPart(models.Model):
    spe_id = models.IntegerField(null=True, blank=True)
    part = models.CharField(max_length=255L, blank=True)
    name = models.CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'mbti_specialty_part'

class Results(models.Model):
    field_id = models.IntegerField(primary_key=True, db_column='_id') # Field renamed because it started with '_'.
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
    class Meta:
        db_table = 'results'

class ReversionRevision(models.Model):
    id = models.IntegerField(primary_key=True)
    manager_slug = models.CharField(max_length=200L)
    date_created = models.DateTimeField()
    user_id = models.IntegerField(null=True, blank=True)
    comment = models.TextField()
    class Meta:
        db_table = 'reversion_revision'

class ReversionVersion(models.Model):
    id = models.IntegerField(primary_key=True)
    revision_id = models.IntegerField()
    object_id = models.TextField()
    object_id_int = models.IntegerField(null=True, blank=True)
    content_type_id = models.IntegerField()
    format = models.CharField(max_length=255L)
    serialized_data = models.TextField()
    object_repr = models.TextField()
    type = models.IntegerField()
    class Meta:
        db_table = 'reversion_version'

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

class SchoolPointSpecialty(models.Model):
    sch_point_spe_id = models.IntegerField(primary_key=True)
    spe_name = models.CharField(max_length=50L)
    class Meta:
        db_table = 'school_point_specialty'

class SchoolPointSpecialtyPart(models.Model):
    spe_id = models.IntegerField()
    part = models.CharField(max_length=10L)
    name = models.CharField(max_length=20L)
    class Meta:
        db_table = 'school_point_specialty_part'

class SchoolSpecialtyRelations(models.Model):
    relation_id = models.IntegerField(primary_key=True)
    school_name = models.CharField(max_length=100L)
    specialty_name = models.CharField(max_length=100L)
    specialty_category = models.CharField(max_length=100L, blank=True)
    school_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'school_specialty_relations'

class SchoolSpecialtyRelationsPart(models.Model):
    spe2 = models.CharField(max_length=30L)
    id = models.IntegerField()
    name = models.CharField(max_length=60L)
    class Meta:
        db_table = 'school_specialty_relations_part'

class XadminBookmark(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=128L)
    user_id = models.IntegerField(null=True, blank=True)
    url_name = models.CharField(max_length=64L)
    content_type_id = models.IntegerField()
    query = models.CharField(max_length=1000L)
    is_share = models.IntegerField()
    class Meta:
        db_table = 'xadmin_bookmark'

class XadminUsersettings(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    key = models.CharField(max_length=256L)
    value = models.TextField()
    class Meta:
        db_table = 'xadmin_usersettings'

class XadminUserwidget(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    page_id = models.CharField(max_length=256L)
    widget_type = models.CharField(max_length=16L)
    value = models.TextField()
    class Meta:
        db_table = 'xadmin_userwidget'

