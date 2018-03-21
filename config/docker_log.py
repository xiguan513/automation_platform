#!/usr/bin/env python
#-*- coding:utf-8 -*-


from config import docker_con
log_tail_line=1000


def DockerLog(Hostname,port,ContainerName):
    #调取所有容器判断健康度，然后返回日志.
    DockerContainerAll = docker_con.Docker_Con(Hostname,port).Docker_Cli()
    return DockerContainerAll.logs(ContainerName,tail=log_tail_line)