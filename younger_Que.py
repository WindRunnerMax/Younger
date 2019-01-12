#python3
# -*- coding: UTF-8 -*-
#***********************
# Powered By Czy
# 多线程，自动打码
# 读文件提问问题
#***********************

import requests
import re
import threading
import os
import random
import socket
import struct
import time
import LoginCode as lg
import base64

#################################################
#五个账号分别为五个线程 
#添加账号或者减少账号注意在文末注注释或添加线程
zh1=""      
pa1=""
zh2=''      
pa2=''
zh3=''      
pa3=''
zh4=''      
pa4=''
zh5=''      
pa5=''
##################################################

url = 'http://sns.qnzs.youth.cn/index/index'
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Referer': 'http://sns.qnzs.youth.cn/index/index',
    'X-FORWARDED-FOR':'',
    'X-Requested-With':'XMLHttpRequest',
    'CLIENT-IP':''
}

count = 0
vc = lg.LoginCode()

def login(user,password):
    password = str(base64.b64encode(password.encode('utf-8')))[2:-1]
    while True:
        IP = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        HEADERS['X-FORWARDED-FOR'] = IP
        HEADERS['CLIENT-IP'] = IP
        
        mysession = requests.Session()
        login_url = 'http://sns.qnzs.youth.cn/index/index'
        html = mysession.post(login_url,timeout=60*4 , headers=HEADERS)
        #print(html.text)
            
        regx=r'/index/captcha.[\S]*"'  
        pattern=re.compile(regx) 
        listurl=re.findall(pattern,repr(html.text)) 
        # print(listurl)
        for url2 in listurl:
            url2='http://sns.qnzs.youth.cn'+url2
            checkcode = mysession.post(url2,timeout=60*4 ,headers=HEADERS)
            with open('./VerifyCode/Info/%s.png' % (user),'wb') as f:
                    f.write(checkcode.content)

        time.sleep(1)
        code = vc.CodeMatch(user)

        param={
                'user[mobile]':'',
                'user[pwd]':'',
                'user[code]':'1234',
                'user[con]':'index',
                'user[id]':'df7d771c'
            }
        param['user[mobile]']=user
        param['user[pwd]']=password
        param['user[code]']=code
        url4='http://sns.qnzs.youth.cn/ajax/login'
        html = mysession.post(url4,data=param, headers=HEADERS)
        #print(html.text)
        o = html.text.find('"err":0,')
        if o is not -1:
            print("CODE MATCH:" + code)
            return mysession
        o = html.text.find('"err":6,')
        if o is not -1:
            print(user + "账号密码错误")
            exit(0)
        pass


def submit(user,password):
    global count
    mysession = login(user,password)
    print(user+'-login success')
    HEADERS['Referer']='http://sns.qnzs.youth.cn/question/ask'
    quesub='http://sns.qnzs.youth.cn/ajax/quessave'
    que={
    'change_aid':'0',
    'change_limit':'0',
    'ques[title]':'',
    'ques[desc]':''
         }
    text="./Question/"+user+".txt"
    try:
        file=open(text,'r+',encoding= 'utf8') ######读取提问问题的文件
    except Exception as e:
        print("文件不存在")
        exit(0)
    while 1:
        line = file.readline()
        if not line:
            break
        print(line,end='')
        que['ques[title]']=line
        que['ques[desc]']=line
        html = mysession.post(quesub,data=que, headers=HEADERS)
        m = html.text.find('"err":0,')
        if m is not -1:
            print(user+"-提交成功",end='\n\n')
            count+=1
            print("LOCAL COUNT:"+str(count))
        n = html.text.find('"err":4,')
        if n is not -1:
            print(user+"-频繁",end='\n\n')
            time.sleep(180)
            html = mysession.post(quesub,data=que, headers=HEADERS)
            m = html.text.find('"err":0,')
            if m is not -1:
                print(user+"-提交成功",end='\n\n')
                count+=1
                print("LOCAL COUNT:"+str(count))
            n = html.text.find('"err":4,')
            if n is not -1:
                print(user+"-频繁",end='\n\n')
        out = html.text.find('"err":1')
        if out is not -1:
            print("Re Login")
            mysession = login(user,password)
            print("Login Sucess")
        time.sleep(660)
    file.close()
       
      
class A(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        submit(zh1,pa1)

class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        submit(zh2,pa2)

class C(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        submit(zh3,pa3)
        
class D(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        submit(zh4,pa4)

class E(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        submit(zh5,pa5)
       
if __name__ == '__main__':
    t1 = A()
    t1.start()
    time.sleep(30)
    t1 = B()
    t1.start()
    time.sleep(30)
    t1 = C()
    t1.start()
    time.sleep(30)
    t1 = D()
    t1.start()
    time.sleep(30)
    t1 = E()
    t1.start()

