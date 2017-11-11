# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Article,Picture
from django.shortcuts import render
from django.http import JsonResponse
import string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def queryset_to_dict(mylist,name)
    thdict = {}
    count = 0
    for l in mylist:
        mydict = {}
        mydict['id'] = l[0]
        mydict['category'] = l[1]
        mydict['title'] = l[2]
        count += 1
        dictname = 'dict' + str(name) + str(count)
        thdict[dictname] = mydict
    return thdict


def homepage(request):
	if request.method == 'GET':
		return JsonResponse({'status': '1', 'msg': 'invalid type'})
	elif request.method == 'POST':
		mylist_xwdt = Article.objects.filter(part='xwdt').order_by('-id').values_list('id', 'category', 'title')[0:6]
		mylist_tzgg = Article.objects.filter(part='tzgg').order_by('-id').values_list('id', 'category', 'title')[0:6]
		mylist_pic = Picture.objects.all().order_by('-id')[0:3]

		listdict = {}
		listdict['xwdt'] = queryset_to_dict(mylist_xwdt, 'xwdt')
		listdict['tzgg'] = queryset_to_dict(mylist_xwdt, 'tzgg')
		picdict = {}
		count = 0
		for t in mylist_pic:
			mydict = {}
			mydict['pic_url'] = 'http://39.106.45.205:8000/site_media/' + str(t.image)
			mydict['news_url'] = t.url
			count += 1
			dictname = 'pic_'  + str(count)
			picdict[dictname] = mydict
		listdict['picture'] = picdict
		#listdict['introduction'] = '一个静态页面，url前端给'
		#状态码
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
