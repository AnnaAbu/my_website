# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Article
from django.shortcuts import render
from django.http import JsonResponse
import string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def homepage(request):
	mylist = Article.objects.order_by('-id').values_list('id', 'title')[0:6]
	listdict = {}
	count = 0
	for l in mylist:
		mydict = {}
		mydict['id'] = l[0]
		mydict['title'] = l[1]
		count += 1
		dictname = 'dict' + str(count)
		listdict[dictname] = mydict
    # 之后需要修改为动态
	listdict['pic_1'] = "http://39.106.45.205:8000/site_media/photos/2017/11/08/picture_1.jpg"
	listdict['pic_2'] = "http://39.106.45.205:8000/site_media/photos/2017/11/08/picture_2.jpg"
	listdict['pic_3'] = "http://39.106.45.205:8000/site_media/photos/2017/11/08/picture_3.jpg"
	listdict['status'] = '0'
	return JsonResponse(listdict)


def getlist(request):
	if request.method == 'GET':
		return JsonResponse({'status': '1', 'msg': 'invalid type'})
	elif request.method == 'POST':
		getpager = request.POST.get('page', 1)		
		getcategory = request.POST.get('category')
		getcategory=getcategory.strip()
		if getcategory==None:
			return JsonResponse({'status': '1', 'msg': 'not found category'})
		page_articlenum = 15
		try:
			getpager=int(getpager)
		except ValueError:
			return JsonResponse({'status':'1','msg':'page is not an Integer'})
		if (getpager - 1) * page_articlenum > Article.objects.count():
			return JsonResponse({'status': '1', 'msg': 'invalid page'})
		elif getpager * page_articlenum < Article.objects.count():
			if getcategory=='all':
				mylist = Article.objects.all().order_by('-id').value_list('id','title','timestamp')[(getpager-1)*page_articlenum:page_articlenum]
			else:
				mylist = Article.objects.filter(category=getcategory).order_by('-id').values_list('id', 'title', 'timestamp')[(getpager-1)*page_articlenum:page_articlenum]
		else:
			if getcategory=='all':
				mylist = Article.objects.all().order_by('-id').value_list('id', 'title', 'timestamp')[(getpager - 1) * page_articlenum:Article.objects.count()-(getpager-1)*page_articlenum]
			else:
				mylist = Article.objects.filter(category=getcategory).order_by('-id').values_list('id', 'title','timestamp')[(getpager - 1) * page_articlenum:Article.objects.count() - (getpager - 1) * page_articlenum]
		if mylist==None:
			return JsonResponse({'status':'1','msg':'invalid category'})
		mydict={}

		# list=[]
            #count = 0
            #for l in mylist:
              #  mydict = {}
               # mydict['id'] = l[0]
               # mydict['title'] = l[1]
               # mydict['timestamp'] = l[2]
                #count += 1
                #dictname = 'dict' + str(count)
                #listdict = mydict
		mydict['status'] = '0'
		mydict['data']=mylist
		return JsonResponse(mydict)
		# elif (page+1)*page_articlenum-Article.objects.count<page_articlenum:
        # list里面就是[page*page_articlenum:Article.object.count-page*page_articlenum]
        # pass
        # else :
        # return JsonResponse({'status':'1','msg':'out of page'})


def detail(request):
	if request.method == 'GET':
		return JsonResponse({'status':'1','msg':'invalid type'})
	elif request.method == 'POST':
		getid = request.POST['id']
	try:
		article = Article.objects.get(id=getid)
	except Article.DoesNotExist:
		return JsonResponse({'status': '1', 'msg': 'id not found'})
	mydict = {}
	for arti in article:
		mydict['id'] = arti.id
		mydict['title'] = arti.title
		mydict['content'] = arti.content
		mydict['timestamp'] = arti.timestamp
	mydict['status'] = '0'
	return JsonResponse(mydict)
