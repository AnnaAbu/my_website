# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.http import JsonResponse
from django.contrib import auth
import time
from django.contrib.auth.decorators import login_required

# Create your views here.


def get_valid_dict(src_dict,src_list):
    desc_dict={}
	for i in src_list:
	    desc_dict[i]=src_dict.get(i,'null')
	return desc_dict

def queryset_to_dictlist(query_set,attrlist):
    if not isinstance(list(query_set), list):
        raise Exception("bad query_set at line "+sys._getframe().f_lineno+" in "+__file__)
    dict_list=[]
    for row in query_set:
        if len(row) !=len(attrlist):
            raise Exception("length of query_set row and attrlist not same at line "+sys._getframe().f_lineno+" in "+__file__)
        temp_dict={}
        for i in range(len(row)):
            temp_dict[attrlist[i]]=row[i]
        dict_list.append(temp_dict)
    return dict_list

def homepage(request):
        mylist_pic = Picture.objects.all().values_list('image').order_by('-id')[0:3]
        listdict = {}
        listdict['data'] = queryset_to_dictlist(mylist_pic,['pic_url'])
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
        dict=get_valid_dict(request.POST,['id',])
    try:
        dict['id']=int(dict['id'])
    except ValueError:
        response= JsonResponse({'status':'1','msg':'id is not an integer'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    try:
        article = Article.objects.get(**dict)
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
        dict=get_valid_dict(request.POST,['title','content','category'])
        dict['timestamp']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    if dict['category'] not in choicelist:
        response = JsonResponse({'status': '1', 'msg': 'bad category'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    else:
        try:
             Article.objects.create(**dict)
        except Exception:
            response = JsonResponse({'status': '1', 'msg': 'invalid attribute'})
            response["Access-Control-Allow-Origin"] = '*'
            return response
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
        dict=get_valid_dict(request.POST,['id','class'])
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
        getid=request.POST.get('id')
        dict=get_valid_dict(request.POST,['title','content','category'])
        dict['timestamp']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    if dict['category'] not in choicelist:
        response = JsonResponse({'status': '1', 'msg': 'bad category'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    else:
        try:
            Article.objects.filter(id=getid).update(**dict)
        except Exception:
            response = JsonResponse({'status': '1', 'msg': 'invalid attribute'})
            response["Access-Control-Allow-Origin"] = '*'
            return response
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
        dict=get_valid_dict(request.POST,['user','password'])
    if auth.authenticate(**dict) is None:
        response = JsonResponse({'status': '1', 'msg': 'bad user or pwd'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    else:
        response = JsonResponse({'status': '0', 'msg': 'login success'})
        response["Access-Control-Allow-Origin"] = '*'
        return response

def research(request):
    mylist_pic = Research.objects.all().values_list('image','title','description').order_by('-id')[0:2]
    listdict = {}
    listdict['data'] = queryset_to_dictlist(mylist_pic, ['pic_url', 'title','description'])
    listdict['status'] = '0'
    response = JsonResponse(listdict)
    response["Access-Control-Allow-Origin"] = '*'
    return response



