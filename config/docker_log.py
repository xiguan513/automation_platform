#!/usr/bin/env python
#-*- coding:utf-8 -*-


from config import docker_con
import datetime
log_tail_line=2000


def DockerLog(Hostname,port,ContainerName,find_time=0):
    #调取所有容器判断健康度，然后返回日志.
    if find_time==0:
        DockerContainerAll = docker_con.Docker_Con(Hostname,port).Docker_Cli()
        return DockerContainerAll.logs(ContainerName,tail=log_tail_line)
    else:
        find_time = int(find_time)
        DatetimeNow = datetime.datetime.now() + datetime.timedelta(minutes=-find_time, hours=-8)
        DockerContainerAll = docker_con.Docker_Con(Hostname,port).Docker_Cli()
        return DockerContainerAll.logs(ContainerName,since=DatetimeNow)