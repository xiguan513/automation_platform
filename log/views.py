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
from django.http import FileResponse
# Create your views here.

path_dir = "dump/"


@login_required
def LogNow(request):
    # 接收前端传递参数进行计算返回渲染后的页面
    if request.method == 'GET':
        Hostname = request.GET.get('hostname')
        ContainerName = request.GET.get('container_name')
        find_time = request.GET.get('find_time')
        log_type = request.GET.get('log_type')
        if log_type != "dump":
            if not find_time:
                Port = DockerServer.objects.values_list("port").filter(ip=Hostname).first()[0]
                logs = docker_log.DockerLog(Hostname,Port,ContainerName)
                logs_str = mark_safe(str(logs, encoding="utf-8"))
                info = {'logs': logs_str,'hostname': Hostname, 'container_name': ContainerName}
                return render(request, 'log/lognow.html', info)
            else:
                Port = DockerServer.objects.values_list("port").filter(ip=Hostname).first()[0]
                logs = docker_log.DockerLog(Hostname,Port,ContainerName,find_time)
                logs_str = mark_safe(str(logs, encoding="utf-8"))
                info = {'logs': logs_str,'hostname': Hostname, 'container_name': ContainerName}
                return render(request, 'log/lognow.html', info)
        if log_type == "dump":
            if not find_time:
                Port = DockerServer.objects.values_list("port").filter(ip=Hostname).first()[0]
                logs = docker_log.DockerLog(Hostname,Port,ContainerName)
                logs_str = mark_safe(str(logs, encoding="utf-8"))
                container = docker_con.Docker_Con(Hostname,Port).Docker_Cli().containers(filters={"id": ContainerName})
                container_name = str([name["Names"] for name in container][0][0].split("/")[1])
                if not os.path.exists(path_dir):
                    os.mkdir(path_dir)
                with open(path_dir+container_name,"w+",encoding="utf-8") as f:
                    f.writelines(logs_str)
                    return file_down(request,path_dir,container_name)
            else:
                Port = DockerServer.objects.values_list("port").filter(ip=Hostname).first()[0]
                logs = docker_log.DockerLog(Hostname,Port,ContainerName,find_time)
                logs_str = mark_safe(str(logs, encoding="utf-8"))
                container = docker_con.Docker_Con(Hostname,Port).Docker_Cli().containers(filters={"id": ContainerName})
                container_name = [name["Names"] for name in container][0][0]
                if not os.path.exists(path_dir):
                    os.mkdir(path_dir)
                with open(path_dir+container_name,"w+",encoding="utf-8") as f:
                    f.writelines(logs_str)
                    return file_down(request,path_dir,container_name)

def file_down(request,path,name):
        file = open(path+name,"rb")
        response =FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Length'] = os.path.getsize(path+name)
        response['Content-Encoding'] = 'utf-8'
        response['Content-Disposition'] = 'attachment;filename="%s"' % name
        return response



