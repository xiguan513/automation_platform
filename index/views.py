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

from config import redis_con
from config import swagger_con
from config import docker_con
from config.models import Dockerenv,DockerServer,ReDoc

# Create your views here.

def UserLogin(request):
    errors = {}
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next')
            print(next_url)
            if next_url:
                return redirect(next_url)
            return redirect('/index')
        else:
            print(errors)
            errors = {'error': 'User Lgin Fail'}
            return render(request, 'login.html', errors)

def UserLogout(request):
    logout(request)
    return HttpResponse("logout")

def index(request):
    env_status = [value for value in Dockerenv.objects.values_list("envname","envdescribe","id").all()]
    return render(request,'index.html',{"env_status":env_status})

def show(request):
    hostname = request.GET["hostname"]
    port = DockerServer.objects.values_list("port").filter(ip=hostname).filter()[0][0]
    containers_status = docker_con.Docker_Con(hostname,port).Docker_Cli().containers(all=True)
    return render(request,'containers_status.html',{"containers_status":containers_status,"ip":hostname})

def status(request):
    start_stop = request.GET["start_stop"]
    return HttpResponse(start_stop)


def redis_index(request):
    return render(request,'redis.html')

def redis(request):
    if request.GET["Redisip"] and request.GET["Rediskey"]:
        redis_ip = request.GET["Redisip"]
        redis_key = request.GET["Rediskey"]
        if redis_ip and redis_key:
            cli = redis_con.redis_cli(redis_ip, '6379').get(redis_key)
            if cli:
                return render(request,'redis.html',{
                    'redis_value':cli.decode("utf-8"),
                    'redis_key': redis_key,
                    'redis_ip': redis_ip,

                    })
            else:
                return render(request,'redis.html',{
                    'redis_key': redis_key,
                    'redis_ip': redis_ip,
                    'redis_value': "Null",
                    })
    if request.GET["flushkey"] and request.GET["Redisip"]:
        redis_ip = request.GET["Redisip"]
        redis_flush_key = request.GET["flushkey"]
        cli = redis_con.redis_cli(redis_ip,'6379')
        cli.delete(redis_flush_key)
        return render(request,'redis.html',{
            'redis_flush_key': redis_flush_key,
            'redis_ip': redis_ip,
            })
    if request.GET["flushdb"] and request.GET["Redisip"]:
        redis_ip = request.GET["Redisip"]
        redis_flush_db = request.GET["flushdb"]
        cli = redis_con.redis_cli(redis_ip,'6379')
        keys = cli.keys()
        print(keys)
        cli.delete(*keys)
        return render(request,'redis.html',{
            'redis_flush_db': redis_flush_db,
            'redis_ip': redis_ip,
            })



def upload(request):
    docker_ip,docker_port = DockerServer.objects.values_list("ip", "port").filter(role="redoc").first()
    cli = docker_con.Docker_Con(docker_ip,docker_port).Docker_Cli()
    if request.method=="POST":
        name = request.POST.get('project')
        print(name)
        if name == "lph":
            docker_name, redoc_url,redoc_path = ReDoc.objects.values_list("dockername", "projecturl","projectpath").filter(
                projectname=name).first()
            swagger_con.handle_upload_file(redoc_url,redoc_path)
            try:
                cli.restart(docker_name)
                docker_containers = cli.containers(filters={"name": docker_name})
                return render(request, 'soucess.html',
                              {'docker_containers': docker_containers})  # 此处简单返回一个成功的消息，在实际应用中可以返回到指定的页面中
            except:
                return HttpResponse("Restart Fail!")
        elif name == "noSignlph":
            docker_name, redoc_url, redoc_path = ReDoc.objects.values_list("dockername", "projecturl",
                                                                           "projectpath").filter(
                projectname=name).first()
            swagger_con.handle_upload_file(redoc_url, redoc_path)
            try:
                cli.restart(docker_name)
                docker_containers = cli.containers(filters={"name": docker_name})
                return render(request, 'soucess.html',
                              {'docker_containers': docker_containers})  # 此处简单返回一个成功的消息，在实际应用中可以返回到指定的页面中
            except:
                return HttpResponse("Restart Fail!")
    project_name = ReDoc.objects.values_list("projectname")
    return render(request,'upload.html',{"project_name":project_name})





