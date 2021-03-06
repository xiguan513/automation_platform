from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,render_to_response
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout,login
import requests
import yaml
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
import os,sys
import django
sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "automation_platform.settings")
django.setup()
from config import redis_con
from config import swagger_con
from config import docker_con
from config.models import Dockerenv,DockerServer,ReDoc



# Create your views here.

@login_required
def env(request):
    envid = request.GET["id"]
    envid = int(envid)
    return render(request, 'ynsy_env.html', {"docker_dict": index_env(envid)[0],"docker_dict": index_env(envid)[1]})


def index_env(id):
    docker_dict = {}
    container_dict = {}
    for vlaue in DockerServer.objects.values_list("ip","port","role").filter(dockerenv_id=id):
        ip,port,role = vlaue
        docker_dict[ip] = role
        container_list = []
        for i in docker_con.Docker_Con(ip, port).Docker_Cli().containers():
            if role == "worker":
                i = i["Names"][0][:-28]
                container_list.append(i)
            else:
                container_list.append(i["Names"][0])
        container_dict[ip] = container_list
    return (docker_dict,container_dict)


@login_required
def start_stop(request):
    ip = request.GET["ip"]
    id = request.GET["id"]
    docker_status = request.GET["docker_status"]
    port = DockerServer.objects.values_list("port").filter(ip=ip).first()[0]
    containers_status = docker_con.Docker_Con(ip, port).Docker_Cli()
    if docker_status == "start":
        if containers_status.start(id):
            return HttpResponse("start fail")
        else:
            return HttpResponse("start sucesss")
    elif docker_status == "stop":
        if containers_status.stop(id):
            return HttpResponse("stop fail")
        else:
            return HttpResponse("stop sucesss")
    elif docker_status == "restart":
        if containers_status.restart(id):
            return HttpResponse("restart fail")
        else:
            return HttpResponse("restart sucesss")


if __name__=="__main__":
    a = "/ynsy_dijie_recruit_provider.1.yccs2uwvclizdvwfz844zrqys"
    b = a[:-28]
    print(b)

