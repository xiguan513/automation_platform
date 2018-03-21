#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os,sys
import django
sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "automation_platform.settings")
django.setup()
import requests
import yaml
import os

from config.models import DockerServer,Dockerenv,ReDoc
from config import docker_con

# Create your tests here.

if __name__=="__main__":
    # for value in [value for value in DockerServer.objects.values_list("ip","port").all()]:
    #     ip,port = value
    #     print(ip,port)
    # docker_start = [value for value in Dockerenv.objects.values_list("envname","envdescribe").all()]
    # print(docker_start)
    #
    # dict_status = {}
    # for vlaue in DockerServer.objects.values_list("ip","port").filter(dockerenv_id=3):
    #     ip,port = vlaue
    #     containers_status = docker_con.Docker_Con(ip, port).Docker_Cli().containers()
    # print(containers_status)


    # for vlaue in DockerServer.objects.values_list("ip","port","role").filter(dockerenv_id=2):
    #     ip,port,role = vlaue
    #     #containers_status = docker_con.Docker_Con(ip,port).Docker_Cli().containers(all=True)
    #     print(ip,port,role)

    docker_ip,docker_port = DockerServer.objects.values_list("ip","port").filter(role="redoc").first()

    cli = docker_con.Docker_Con(docker_ip, docker_port).Docker_Cli()



    # name = "lph"
    # docker_name, redoc_url, redoc_path = ReDoc.objects.values_list("dockername", "projecturl", "projectpath").filter(
    #     projectname=name).first()
    #
    # def handle_upload_file(procurl, path):
    #     project_path = path  # 上传文件的保存路径，可以自己指定任意的路径
    #     project_data = requests.get(url=procurl)
    #     if not os.path.exists(project_path):
    #         os.makedirs(project_path)
    #     with open(project_path + "swagger.yaml", "w") as destination:
    #         yaml.dump(project_data.json(), destination)
    #
    # print(redoc_url,redoc_path)
    # handle_upload_file(redoc_url, redoc_path)