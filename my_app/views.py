# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.http import JsonResponse
from django.contrib import auth
import time
from django.contrib.auth.decorators import login_required

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

def get_attr(request,list):
    dict={}
    for l in list:
        dict[l]=request.POST.get(l,None)
    return dict

def homepage(request):
        mylist_pic = Picture.objects.all().values_list('id','image').order_by('-id')[0:3]
        listdict = {}
        listdict['picture'] = queryset_to_dictlist(mylist_pic,['id','pic_url'])
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
        response = JsonResponse({'status': '1', 'msg': 'invalid type'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
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
        response = JsonResponse({'status': '1', 'msg': 'invalid type'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    elif request.method == 'POST':
        dict=get_attr(request,['id',])
    try:
        dict['id']=int(dict['id'])
    except ValueError:
        response= JsonResponse({'status':'1','msg':'id is not an integer'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    try:
        article = Article.objects.get(dict)
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

@login_required()
def add_article(request):
    if request.method=='GET':
        response = JsonResponse({'status': '1', 'msg': 'invalid type'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    elif request.method=='POST':
        dict=get_attr(request,['title','content','category'])
        dict['timestamp']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    try:
         Article.objects.create(dict)
    except Exception:
        response = JsonResponse({'status': '1', 'msg': 'invalid attribute'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    finally:
        response=JsonResponse({'status':'0','msg':'request complete'})
        response["Access-Control-Allow-Origin"] = '*'
        return response

@login_required()
def delete_object(request):
    if request.method=='GET':
        response = JsonResponse({'status': '1', 'msg': 'invalid type'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    elif request.method=='POST':
        getid=request.POST.get['id']
        getclass=request.GET.get['class']
        dict=get_attr(request,['id','class'])
    if dict['class']=='Article':
        try:
            this_object=Article.objects.get(id=dict['id'])
            this_object.delete()
        except Exception:
            response = JsonResponse({'status': '1', 'msg': 'invalid id'})
            response["Access-Control-Allow-Origin"] = '*'
            return response
    elif dict['class']=='Picture':
        try:
            this_object=Picture.objects.get(id=dict['id'])
            this_object.delete()
        except Exception:
            response=JsonResponse({'status':'1','msg':'invalid id'})
            response["Access-Control-Allow-Origin"] = '*'
            return response
    else:
        response = JsonResponse({'status': '1', 'msg': 'invalid class'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    response=JsonResponse({'status':'0','msg':'request complete'})
    response["Access-Control-Allow-Origin"] = '*'
    return response

@login_required()
def update_article(request):
    if request.method=='GET':
        response = JsonResponse({'status': '1', 'msg': 'invalid type'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    elif request.method == 'POST':
        getid=request.POST.get['id']
        dict=get_attr(request,['title','content','category'])
        dict['timestamp']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    try:
        Article.objects.filter(id=getid).update(dict)
    except Exception:
        response = JsonResponse({'status': '1', 'msg': 'invalid attribute'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    finally:
        response = JsonResponse({'status': '0', 'msg': 'request complete'})
        response["Access-Control-Allow-Origin"] = '*'
        return response

@login_required()
def pic_save(request):
    if request.method=='GET':
        response = JsonResponse({'status': '1', 'msg': 'invalid type'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    elif request.method=='POST':
        new_img = Picture(
            image=request.FILES.get('img'),
            name=request.FILES.get('img').name
        )
        new_img.save()
        response=JsonResponse({'status':'0','msg':'request complete'})
        response["Access-Control-Allow-Origin"] = '*'
        return response


def login(request):
    if request.method=='GET':
        response = JsonResponse({'status': '1', 'msg': 'invalid type'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    elif request.method == 'POST':
        dict=get_attr(request,['user','password'])
    if auth.authenticate(dict) is None:
        response = JsonResponse({'status': '1', 'msg': 'bad user or pwd'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    else:
        response = JsonResponse({'status': '0', 'msg': 'login success'})
        response["Access-Control-Allow-Origin"] = '*'
        return response




