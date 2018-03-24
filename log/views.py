#-*- coding:utf-8 -*-
import os
import sys
import importlib
importlib.reload(sys)
from django.shortcuts import render,HttpResponse
from django.http import StreamingHttpResponse
from django.utils.safestring import mark_safe
import datetime
import os,zipfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from collections import deque
from config import docker_log,docker_con
from config.models import DockerServer,Dockerenv,ReDoc
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def LogNow(request):
    # 接收前端传递参数进行计算返回渲染后的页面
    if request.method == 'GET':
        Hostname = request.GET.get('hostname')
        ContainerName = request.GET.get('container_name')
        Port = DockerServer.objects.values_list("port").filter(ip=Hostname).first()[0]
        logs = docker_log.DockerLog(Hostname,Port,ContainerName)
        logs_str = mark_safe(str(logs, encoding="utf-8"))
        info = {'logs': logs_str,'hostname': Hostname, 'container_name': ContainerName}
        return render(request, 'log/lognow.html', info)








