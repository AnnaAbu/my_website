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
    for l in mylist:
        count=0
        mydict = {}
        for k in attrlist:
            mydict[k]=l[count]
            count+=1
        list.append(mydict)
    return  list


def homepage(request):
        mylist_pic = Picture.objects.all().order_by('-id')[0:3]
        listdict = {}
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
        response= JsonResponse(listdict)
        response["Access-Control-Allow-Origin"]='*'
        return response


def getlist(request):
    if request.method == 'GET':
        print(request.GET)
        import ipdb;ipdb.set_trace()
        getpage= request.GET.get('page',1)
        getcategory=request.GET.get('category')
        getnum=request.GET.get('num',3)
    elif request.method == 'POST':
        getpage = request.POST.get('page', 1)        
        getcategory = request.POST.get('category')
        getnum=request.POST.get('num',3)
    #getcategory=getcategory.strip()
    if getcategory==None:
        response= JsonResponse({'status': '1', 'msg': 'not found category'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    if isinstance(getcategory,list):
        response= JsonResponse({'status':'1','msg':'invalid type'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    #page_articlenum = 15
    try:
        getpage=int(getpage)
        getnum=int(getnum)
        getcategory=eval(getcategory)
    except ValueError:
        response= JsonResponse({'status': '1', 'msg': 'page or num is not an Integer'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    except SyntaxError:
        response= JsonResponse({'status':'1','msg':'invalid category'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    except NameError:
        response= JsonResponse({'status':'1','msg':'invalid category'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    mydict={}

    for l in getcategory:
        if Article.objects.filter(category=l).count()==0:
            response= JsonResponse({'status':'1','msg':'invalid category'})
            response["Access-Control-Allow-Origin"] = '*'
            return response
        backlist=[]
        if (getpage - 1) * getnum > Article.objects.filter(category=l).count():
            response= JsonResponse({'status': '1', 'msg': 'invalid page or num'})
            response["Access-Control-Allow-Origin"] = '*'
            return response
        elif getpage*getnum<Article.objects.filter(category=l).count():
            mylist=Article.objects.filter(category=l).order_by('-id').values_list('category','id','title','timestamp')[(getpage-1)*getnum:getnum]
        else:
            mylist=Article.objects.filter(category=l).order_by('-id').values_list('category','id','title','timestamp')[
                   (getpage-1)*getnum:Article.objects.filter(category=l).count()-(getpage-1)*getnum]
        mydict[l]=queryset_to_dictlist(mylist,['category','id','title','timestamp'])

    #elif getpage * getnum < Article.objects.count():

        '''
        if getcategory=='all':
            mylist = Article.objects.all().order_by('-id').values_list('id','title','timestamp')[(getpage-1)*page_articlenum:page_articlenum]
        else:
            mylist = Article.objects.filter(category=getcategory).order_by('-id').values_list('id', 'title', 'timestamp')[(getpage-1)*page_articlenum:page_articlenum]
    else:
        if getcategory=='all':
            mylist = Article.objects.all().order_by('-id').values_list('id', 'title', 'timestamp')[(getpage - 1) * page_articlenum:Article.objects.count()-(getpage-1)*page_articlenum]
        else:
            mylist = Article.objects.filter(category=getcategory).order_by('-id').values_list('id', 'title','timestamp')[(getpage - 1) * page_articlenum:Article.objects.count() - (getpage - 1) * page_articlenum]
        
    mydict={}

    list=[]
    for l in mylist:
        dict = {}
        dict['id'] = l[0]
        dict['title'] = l[1]
        dict['timestamp'] = l[2]
        list.append(dict)
    if list==[]:
        response= JsonResponse({'status': '1', 'msg': 'invalid category'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
        '''
    mydict['status'] = '0'
    #mydict['data']=list
    response= JsonResponse(mydict)
    response["Access-Control-Allow-Origin"] = '*'
    return response
        # elif (page+1)*page_articlenum-Article.objects.count<page_articlenum:
        # list里面就是[page*page_articlenum:Article.object.count-page*page_articlenum]
        # pass
        # else :
        # response= JsonResponse({'status':'1','msg':'out of page'})


def detail(request):
    if request.method == 'GET':
        getid=request.GET.get('id')
        #response= JsonResponse({'status':'1','msg':'invalid type'})
    elif request.method == 'POST':
        getid = request.POST['id']
    try:
        getid=int(getid)
    except ValueError:
        response= JsonResponse({'status':'1','msg':'id is not an integer'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    try:
        article = Article.objects.get(id=getid)
    except Article.DoesNotExist:
        response= JsonResponse({'status': '1', 'msg': 'id not found'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    mydict = {}
    mydict['id'] = article.id
    mydict['title'] = article.title
    mydict['content'] = article.content
    mydict['timestamp'] = article.timestamp
    mydict['status'] = '0'
    response= JsonResponse(mydict)
    response["Access-Control-Allow-Origin"] = '*'
    return response
