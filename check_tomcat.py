#!/usr/bin/env python

import platform
import os
import requests
import time

def log(s):
    print('%s > %s' % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),s))

class tomcat_control():
    def __init__(self,path):
        self.path = path
        osmap = {'Windows':'.bat', 'Linux':'.sh'}
        self.ext = osmap[platform.system()]
    def shutdown(self):
        cmd = '%sshutdown%s' % (self.path,self.ext)
        log(cmd)
        os.system(cmd)
    def startup(self):
        cmd = '%sstartup%s' % (self.path,self.ext)
        log(cmd)
        os.system(cmd)

class check_modle():
    def __init__(self,url):
        self.url = url
        self.statusdic = {}
        self.reset()
    def reset(self):
        self.success_count = 0
        self.fail_count = 0
    def http_code(self):
        try :
            code = str(requests.get(self.url, timeout=10).status_code)
        except Exception as e:
            log(e)
            code = '000'
        log(code)
        return code
    def check(self):
        while(1):
            code = self.http_code()
            self.statusdic[str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))] = code
            if code == '200':
                self.success_count+=1
            else :
                self.fail_count+=1
            if self.success_count >= 10 :
                self.reset()
                return False
            if self.fail_count >= 6 :
                self.reset()
                return True
            time.sleep(1)
    def check_log(self):
        print('-'*20)
        for k in self.statusdic.keys():
            print('%s <check_log> %s' % (k,self.statusdic[k]))
        print('-'*20)
        self.statusdic = {}
if __name__ == '__main__':
    if platform.system() == 'Windows':
        os.system("title TOMCAT CHECK")
    check_url = 'http://127.0.0.1:8080/'
    tomcat_path = 'F:/apache-tomcat-8.5.39/bin/'
    #tomcat_path = '/opt/apache-tomcat-8.5.39/bin'
    os.chdir(tomcat_path)
    check = check_modle(check_url)
    tomcat = tomcat_control(tomcat_path)
    while(1):
        if check.check():
            tomcat.shutdown()
            time.sleep(1)
            tomcat.startup()
            time.sleep(30)
        check.check_log()
        time.sleep(30)
