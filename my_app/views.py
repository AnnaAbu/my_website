# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Article,Picture
from django.http import JsonResponse
from django.forms.models import model_to_dict  
import math



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
        listdict['picture'] = queryset_to_dictlist(mylist_pic,['pic_url','news_url'])
        listdict['status'] = '0'
        response= JsonResponse(listdict)
        response["Access-Control-Allow-Origin"]='*'
        return response
def getdata(page,num,category):
    args_key=('category','id','title','timestamp')
    if category=="all":
        query_set=Article.objects.order_by('-id').values_list(*args_key)
    else: 
        query_set=Article.objects.filter(category=category).order_by('-id').values_list(*args_key)
    count=query_set.count()
    if (count/num < page):
        page=int(count/num)
    return queryset_to_dictlist(query_set[page*num:(page+1)*num],args_key)

def getlist(request):
    if request.method == 'GET':
        page= request.GET.get('page',1)
        categories=request.GET.getlist('category[]')
        num=request.GET.get('num',3)

    elif request.method == 'POST':
        page = request.POST.get('page', 0)        
        categories = request.POST.getlist('category[]',['all',])
        num=request.POST.get('num',3)

    try:
        page=int(page)
        num=int(num)
    except Exception:
        response= JsonResponse({'status': '1', 'msg': 'invalid parameter'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    data={}
    #import ipdb;ipdb.set_trace()
    if "all" in categories:
        data['all']=getdata(page,num,"all")
    else:
        for category in categories:
            data[category]=getdata(page,num,category)
    response= JsonResponse({'status':'0','data':data})
    response["Access-Control-Allow-Origin"] = '*'
    return response

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
