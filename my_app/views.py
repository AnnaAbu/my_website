# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Article,Picture
from django.http import JsonResponse


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
    if getcategory==None:
        response= JsonResponse({'status': '1', 'msg': 'not found category'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    if isinstance(getcategory,list):
        response= JsonResponse({'status':'1','msg':'invalid type'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    try:
        getpage=int(getpage)
        getnum=int(getnum)
        getcategory=eval(getcategory)
    except ValueError:
        response= JsonResponse({'status': '1', 'msg': 'page or num is not an Integer'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    except (SyntaxError,NameError):
        response= JsonResponse({'status':'1','msg':'invalid category'})
        response["Access-Control-Allow-Origin"] = '*'
        return response
    mydict={}
    for l in getcategory:
        l.strip()
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
    mydict['status'] = '0'
    response= JsonResponse(mydict)
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
