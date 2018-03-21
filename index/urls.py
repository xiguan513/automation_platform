#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.UserLogin,name='UserLogin'),
    path('logout/',views.logout,name='logout'),
    path('index/',views.index,name='index'),
    path('status/',views.status,name='status'),
    path(r'upload/', views.upload, name='upload'),
    path(r'redis/', views.redis_index, name='redis_index'),
    path(r'redis/redis_db', views.redis, name='redis'),
    path(r'show/', views.show, name='show'),
    path(r'logout/', views.UserLogout, name='logout'),
]
