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


def env(request):
    envid = request.GET["id"]
    envid = int(envid)
    return render(request, 'ynsy_env.html', {"docker_dict": index_env(envid)})


def index_env(id):
    docker_dict = {}
    for vlaue in DockerServer.objects.values_list("ip","port","role").filter(dockerenv_id=id):
        ip,port,role = vlaue
        docker_dict[ip] = role
    return docker_dict

