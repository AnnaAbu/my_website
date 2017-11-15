"""my_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from my_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', views.login),
	url(r'^homepage',views.homepage),
	url(r'^getlist$',views.getlist),
	url(r'^getlist/detail$',views.detail),
	url(r'^admin/logout$',views.logout),
	url(r'^admin/article/add$',views.add_article),
	url(r'^admin/article$',views.getlist),
	url(r'^admin/article/detail$',views.detail),
	url(r'^admin/article/detail/modify$',views.update_article),
	url(r'^admin/article/detail/delete$',views.delete_object),
	url(r'^admin/picture$',views.homepage),
	url(r'^admin/picture/add$',views.pic_save),
	url(r'^admin/picture/detail/delete$',views.delete_object),
	url(r'^admin/picture$',views.getpictlist)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
