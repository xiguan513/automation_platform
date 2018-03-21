#!/usr/bin/env python
#-*- coding:utf-8 -*-

import requests
import yaml
import os
def handle_upload_file(procurl,path):
    project_path = path  # 上传文件的保存路径，可以自己指定任意的路径
    project_data = requests.get(url=procurl)
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    with open(project_path + "swagger.yaml", "w") as destination:
        yaml.dump(project_data.json(), destination)




if __name__ == "__main__":
    with open('swagger.yaml','rb') as f:
        load = yaml.load(f)
    a = requests.get(url="http://lvphapp.ynsytest.com/v2/api-docs?group=lph")
    with open("swagger.yaml", "w") as f:
        yaml.dump(a.json(), f)