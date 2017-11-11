# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Article(models.Model):
	Category_Choice=(
		('1','实验室简介'),
		('2','新闻动态'),
		('3','通知公告'),
	)
	student_category=(
		('1','本科生')
		('2','研究生')
		('3','博士生')
	)
	id = models.AutoField(primary_key=True)
	title = models.CharField('标题',max_length=255, blank=True)
	content = models.TextField('文章内容')
	timestamp = models.CharField('时间',max_length=20, blank=True)
	category=models.CharField('文章分类',max_length=1,choices=Category_Choice)
	student_category=models.CharField('学生分类',max_length=1,choices=student_category)
	class Meta:
		db_table='article'
class Picture(models.Model):
	id = models.AutoField(primary_key=True)
	image = models.ImageField(upload_to = "photos/%Y/%m/%d")	
	url=models.CharField('对应网址',max_length=100)
	class Meta:
		db_table='picture'

