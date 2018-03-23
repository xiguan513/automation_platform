#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.env,name='env'),
    path(r'start_stop/', views.start_stop, name='start_stop'),
]
