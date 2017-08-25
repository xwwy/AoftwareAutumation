#!/usr/bin/env python
# _*_ coding:utf8 _*_
"""
把jenkins上打包的文件直接上传到omp中

"""
import sys
import requests

def uploads(ip, name, direction):
    """
    根据参数上传，一次上传一个文件

    """
    login_url = "http://{}:7500/omp/api/v1/user/login".format(ip)
    login_data = {
        "username":"admin",
        "passwd":"b2276e9e1597b1efb651c6b55744c9ab"
    }
    login_headers = {
        "Content-Type": "application/json"
    }
    connect = requests.Session()
    connect.post(url=login_url, json=login_data, headers=login_headers) #获取cookies
    connect.headers.popitem()    #上传文件的时requests会自己添加headers，自己添加的headers先删掉
    with open(direction + name, 'rb') as targz:
        files = {
            'file': targz
            }
        upload_url = "http://{}:7500/omp/api/v1/pkgs/upload".format(ip)
        upload = connect.post(upload_url, files=files, timeout=None)
    if upload.status_code == 200:
        analyze = connect.get(
            'http://{0}:7500/omp/api/v1/pkgs/analysis?fileName={1}'.format(ip, name),
            data={"fileName": name}
            )                              #获取校验结果
        if analyze.status_code == 200:
            print "upload and analyze success!"
        else:
            print "upload success but analyze failed"
    else:
        print "upload failed"

if __name__ == "__main__":
    uploads(sys.argv[1], sys.argv[2], sys.argv[3])
