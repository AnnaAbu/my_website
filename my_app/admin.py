# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Article,Picture,Research

# Register your models here.
admin.site.register(Article)
admin.site.register(Picture)
admin.site.register(Research)

