# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

class Author(models.Model):
	id = models.IntegerField(primary_key=True)
	last_name = models.CharField(max_length=150)
	first_names = models.CharField(max_length=300, blank=True)
	birth_year = models.CharField(max_length=10, blank=True)
	death_year = models.CharField(max_length=10, blank=True)
	class Meta:
		managed = False
		db_table = 'library_author'

class Book(models.Model):
	id = models.IntegerField(primary_key=True)
	title = models.CharField(max_length=500)
	subtitle = models.CharField(max_length=500, blank=True)
	author = models.ForeignKey(Author)
	license = models.ForeignKey('License')
	language = models.CharField(max_length=10)
	sha1 = models.CharField(max_length=64, blank=True)
	downloads = models.IntegerField()
	class Meta:
		managed = False
		db_table = 'library_book'

class Bookcover(models.Model):
	id = models.IntegerField(primary_key=True)
	book_id = models.IntegerField()
	cover = models.CharField(max_length=500, blank=True)
	vote = models.IntegerField()
	class Meta:
		managed = False
		db_table = 'library_bookcover'

class Booklcc(models.Model):
	id = models.IntegerField(primary_key=True)
	book_id = models.IntegerField()
	lcc = models.CharField(max_length=8)
	class Meta:
		managed = False
		db_table = 'library_booklcc'

class Booklcsh(models.Model):
	id = models.IntegerField(primary_key=True)
	book_id = models.IntegerField()
	lcsh = models.CharField(max_length=512)
	class Meta:
		managed = False
		db_table = 'library_booklcsh'

class Format(models.Model):
	id = models.IntegerField(primary_key=True)
	mime = models.CharField(max_length=100)
	images = models.IntegerField()
	pattern = models.CharField(max_length=100)
	class Meta:
		managed = False
		db_table = 'library_format'

class Lcc(models.Model):
	id = models.IntegerField(primary_key=True)
	lcc = models.CharField(max_length=8)
	is_subclass = models.IntegerField()
	description = models.CharField(max_length=512, blank=True)
	description_cn = models.CharField(max_length=512, blank=True)
	class Meta:
		managed = False
		db_table = 'library_lcc'

class License(models.Model):
	slug = models.CharField(primary_key=True, max_length=20)
	name = models.CharField(max_length=255)
	class Meta:
		managed = False
		db_table = 'library_license'

class ViewCategory(models.Model):
	id = models.IntegerField(primary_key=True)
	lcc = models.CharField(max_length=8)
	is_subclass = models.IntegerField()
	description = models.CharField(max_length=512, blank=True)
	description_cn = models.CharField(max_length=512, blank=True)
	book_id = models.IntegerField(blank=True, null=True)
	cnt = models.BigIntegerField()
	class Meta:
		managed = False
		db_table = 'library_view_category'

class ViewBooklist(models.Model):
	id = models.IntegerField(primary_key=True)
	title = models.CharField(max_length=500)
	subtitle = models.CharField(max_length=500, blank=True)
	language = models.CharField(max_length=10)
	downloads = models.IntegerField()
	cover = models.CharField(max_length=500, blank=True)
	vote = models.IntegerField()
	last_name = models.CharField(max_length=150)
	first_names = models.CharField(max_length=300, blank=True)
	lcc = models.CharField(max_length=8, blank=True)
	class Meta:
		managed = False
		db_table = 'library_view_booklist'


######################################################################
## user related section

class UserBooklist(models.Model):
	user = models.ForeignKey(User)
	book = models.ForeignKey(Book)
	position = models.CharField(max_length=255)
	class Meta:
		db_table = 'library_user_booklist'

class UserBooklistCurrent(models.Model):
	user = models.OneToOneField(User)
	book = models.ForeignKey(Book, blank=True)

	class Meta:
		db_table = 'library_user_booklist_current'