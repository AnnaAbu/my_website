# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Article,Picture
from django.shortcuts import render
from django.http import JsonResponse
import string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def queryset_to_dictlist(mylist,attrlist):
	list=[]
	count=0
	for l in mylist:
		mydict = {}
		for k in attrlist:
			mydict[k]=l[count]
			count+=1
		list.append(mydict)
	return list


def homepage(request):
	#if request.method == 'GET':
		#return JsonResponse({'status': '1', 'msg': 'invalid type'})
	#elif request.method == 'POST':
		#mylist_xwdt = Article.objects.filter(category='2').order_by('-id').values_list('id', 'student_category', 'title')[0:6]
		#mylist_tzgg = Article.objects.filter(category='1').order_by('-id').values_list('id', 'student_category', 'title')[0:6]
		mylist_pic = Picture.objects.all().order_by('-id')[0:3]
		listdict = {}
		##listdict['tzgg'] = queryset_to_dictlist(mylist_xwdt, 'tzgg')
		piclist=[]
		for t in mylist_pic:
			mydict = {}
			mydict['pic_url'] = '/site_media/' + str(t.image)
			mydict['news_url'] = t.url
			piclist.append(mydict)
		listdict['picture'] = piclist
		#listdict['introduction'] = '一个静态页面，url前端给'
		#状态码
		listdict['status'] = '0'
		return JsonResponse(listdict)



def getlist(request):
	if request.method == 'GET':
		getpager= request.GET.get('page',1)
		getcategory=request.GET.get('category')
		getnum=request.GET.get('num',3)
		#return JsonResponse({'status': '1', 'msg': 'invalid type'})
	elif request.method == 'POST':
		getpager = request.POST.get('page', 1)		
		getcategory = request.POST.get('category')
		getnum=request.POST.get('num',3)
	#getcategory=getcategory.strip()
	if getcategory==None:
		return JsonResponse({'status': '1', 'msg': 'not found category'})
	if isinstance(getcategory,list):
		return JsonResponse({'status':'1','msg':'invalid type'})
	#page_articlenum = 15
	try:
		getpager=int(getpager)
		getnum=int(getnum)
	except ValueError:
		return JsonResponse({'status': '1', 'msg': 'page or num is not an Integer'})

	mydict={}
	for l in getcategory:
		if Article.objects.filter(category=l).count()==0:
			return JsonResponse({'status':'0','msg':'invalid category'})
		backlist=[]
		if (getpager - 1) * getnum >= Article.objects.filter(category=l).count():
			return JsonResponse({'status': '1', 'msg': 'invalid page or num'})
		elif getpager*getnum<Article.objects.filter(category=l).count():
			mylist=Article.objects.filter(category=l).order_by('-id').values_list('category','id','title','timestamp')[(getpager-1)*getnum:getnum]
		else:
			mylist=Article.objects.filter(category=l).order_by('-id').values_list('category','id','title','timestamp')[
				   (getpager-1)*getnum:Article.objects.filter(category=l).count()-(getpager-1)*getnum]
		mydict[l]=queryset_to_dictlist(mylist,['category','id','title','timestamp'])

	#elif getpager * getnum < Article.objects.count():

		'''
		if getcategory=='all':
			mylist = Article.objects.all().order_by('-id').values_list('id','title','timestamp')[(getpager-1)*page_articlenum:page_articlenum]
		else:
			mylist = Article.objects.filter(category=getcategory).order_by('-id').values_list('id', 'title', 'timestamp')[(getpager-1)*page_articlenum:page_articlenum]
	else:
		if getcategory=='all':
			mylist = Article.objects.all().order_by('-id').values_list('id', 'title', 'timestamp')[(getpager - 1) * page_articlenum:Article.objects.count()-(getpager-1)*page_articlenum]
		else:
			mylist = Article.objects.filter(category=getcategory).order_by('-id').values_list('id', 'title','timestamp')[(getpager - 1) * page_articlenum:Article.objects.count() - (getpager - 1) * page_articlenum]
		
	mydict={}

	list=[]
	for l in mylist:
		dict = {}
		dict['id'] = l[0]
		dict['title'] = l[1]
		dict['timestamp'] = l[2]
		list.append(dict)
	if list==[]:
		return JsonResponse({'status': '1', 'msg': 'invalid category'})
		'''
	mydict['status'] = '0'
	#mydict['data']=list
	return JsonResponse(mydict)
		# elif (page+1)*page_articlenum-Article.objects.count<page_articlenum:
        # list里面就是[page*page_articlenum:Article.object.count-page*page_articlenum]
        # pass
        # else :
        # return JsonResponse({'status':'1','msg':'out of page'})


def detail(request):
	if request.method == 'GET':
		getid=request.GET.get('id')
		#return JsonResponse({'status':'1','msg':'invalid type'})
	elif request.method == 'POST':
		getid = request.POST['id']
	try:
		getid=int(getid)
	except ValueError:
		return JsonResponse({'status':'1','msg':'id is not an integer'})
	try:
		article = Article.objects.get(id=getid)
	except Article.DoesNotExist:
		return JsonResponse({'status': '1', 'msg': 'id not found'})
	mydict = {}
	mydict['id'] = article.id
	mydict['title'] = article.title
	mydict['content'] = article.content
	mydict['timestamp'] = article.timestamp
	mydict['status'] = '0'
	return JsonResponse(mydict)