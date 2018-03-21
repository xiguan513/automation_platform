#!/usr/bin/env python
#-*- coding:utf-8 -*-

import redis

def redis_cli(host,port):
    try:
        return redis.Redis(host=host,port=port,db=0)##如果设置了密码，就加上password=密码
    except redis.ConnectionError as rediserror:
        return (rediserror)
