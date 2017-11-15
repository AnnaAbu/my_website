# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Article(models.Model):
	Category_Choice=(
		('kydt','科研动态'),
		('yjcg','研究成果'),
		('bks','本科生'),
		('yjs','研究生'),
		('bss','博士生'),
	)
	id = models.AutoField(primary_key=True)
	title = models.CharField('标题',max_length=255, blank=True)
	content = models.TextField('文章内容')
	timestamp = models.CharField('时间',max_length=25, blank=True)
	category=models.CharField('文章分类',max_length=20,choices=Category_Choice)
	class Meta:
		db_table='article'
class Picture(models.Model):
	id = models.AutoField(primary_key=True)
	image = models.ImageField(upload_to = "photos")
	name = models.CharField('图片名称',max_length=25)
	class Meta:
		db_table='picture'

