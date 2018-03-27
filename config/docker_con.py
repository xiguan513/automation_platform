#!/usr/bin/env python
#-*- coding:utf-8 -*-


import docker
import sys
import random



class Docker_Con(object):
    def __init__(self,docker_ip,docker_port):
        self.docker_ip = docker_ip
        self.docker_port = docker_port

    def Docker_Cli(self):
        self.client = docker.APIClient(base_url='tcp://%s:%s' %  (self.docker_ip,self.docker_port))
        return self.client

if __name__=="__main__":

    a = Docker_Con("192.168.1.136","5555").Docker_Cli().containers(filters={"id":"3326dda5d38e"})
    b = [name["Names"] for name in a][0][0].split("/")[1]
    print(b)