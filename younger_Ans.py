#python3
# -*- coding: UTF-8 -*-
#***********************
# Powered By Czy
# 多线程自动打码
# 回答问题
#***********************

import requests
import re
import threading
import os
import random
import socket
import struct
import time
import base64
import LoginCode as lg

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
    'Referer': 'http://sns.qnzs.youth.cn/',
    'X-FORWARDED-FOR':'',
    'X-Requested-With':'XMLHttpRequest',
    'CLIENT-IP':''
        }
param={
        'user[mobile]':'',
        'user[pwd]':'',
        'user[code]':'1234',
        'user[con]':'index',
        'user[id]':'df7d771c'
    }
param2={
    "change_aid":"0",
    "change_limit":"0",
    "answer[qid]":"31378359",
    "answer[anonymous]":"1",
    "answer[content]":""
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
            print("账号密码错误")
            exit(0)
        pass

def submit_Nextpage(zh,pa,page,HEADERS,mysession,param2,n):
    global count
    HEADERS['Referer']='http://sns.qnzs.youth.cn/index/hot'
    url5='http://sns.qnzs.youth.cn/index/hotlist/page/'+str(page)
    html = mysession.get(url5,headers=HEADERS)
    #print(html.text)
    regx3=r'/index/show/.[\S]*"'  
    pattern3=re.compile(regx3) 
    listurl3=re.findall(pattern3,repr(html.text)) 
    #print(listurl3)
    sum=0
    for url6 in listurl3:
        if sum % 3 is 0 :
           ans_id=url6[15:-1]
           #print (ans_id)
           HEADERS['Referer']='http://sns.qnzs.youth.cn'+url6
           url6='http://sns.qnzs.youth.cn'+url6
           url6 = url6.split("\"")[0]
           print(url6)
           html = mysession.get(url6,headers=HEADERS)
           #print(html.text)
           regx2=r'<p>.[\S]*</p>'  
           pattern2=re.compile(regx2) 
           listurl2=re.findall(pattern2,repr(html.text)) 
           #print(listurl2)
           num=0
           ran=random.randint(8, 15)
           for ans in listurl2:
               num=num+1
               if num<ran :
                   continue
               url7='http://sns.qnzs.youth.cn/ajax/anssave'
               param2['answer[qid]']=ans_id
               param2['answer[content]']=ans
               html = mysession.post(url7,data=param2 , headers=HEADERS)
               print(ans+" page:"+str(page))
               oo = html.text.find('"err":0,')
               if oo is not -1:
                   print(zh+'-回答成功\n')
                   count+=1
                   print("LOCAL COUNT:"+str(count))
               ooo = html.text.find('"err":4,')
               if ooo is not -1:
                   print(zh+'-频繁\n')
               break
               out = html.text.find('"err":1')
               if out is not -1:
                  print("ReLogin")
                  mysession = login(user,password)
                  print("Login Sucess")
           time.sleep(300)
        sum=sum+1
    page=page+1
    submit_Nextpage(zh,pa,page,HEADERS,mysession,param2,n)

def submit(user,password,page,n):
    global count
    mysession = login(user,password)
    print(user+'-login success')
    HEADERS['Referer']='http://sns.qnzs.youth.cn/index/hot'
    url5='http://sns.qnzs.youth.cn/index/hotlist/page/'+str(page)
    html = mysession.get(url5,headers=HEADERS)
    #print(html.text)
    regx3=r'/index/show/.[\S]*"'  
    pattern3=re.compile(regx3) 
    listurl3=re.findall(pattern3,repr(html.text)) 

    sum=0
    for url6 in listurl3:
        if sum % 3 is 0 :
           ans_id=url6[15:-1]
           #print (ans_id)
           HEADERS['Referer']='http://sns.qnzs.youth.cn'+url6
           url6='http://sns.qnzs.youth.cn'+url6
           url6 = url6.split("\"")[0]
           print(url6)
           html = mysession.get(url6,headers=HEADERS)
           #print(html.text)
           regx2=r'<p>.[\S]*</p>'  
           pattern2=re.compile(regx2) 
           listurl2=re.findall(pattern2,repr(html.text)) 
           #print(listurl2)
           num=0
           ran=random.randint(8, 15)
           for ans in listurl2:
               num=num+1
               if num<ran :
                   continue
               url7='http://sns.qnzs.youth.cn/ajax/anssave'
               param2['answer[qid]']=ans_id
               param2['answer[content]']=ans
               html = mysession.post(url7,data=param2 , headers=HEADERS)
               print(ans+" page:"+str(page))
               oo = html.text.find('"err":0,')
               if oo is not -1:
                   print(user+'-回答成功\n')
                   count+=1
                   print("LOCAL COUNT:"+str(count))
               ooo = html.text.find('"err":4,')
               if ooo is not -1:
                   print(user+'-频繁\n')
               break
               out = html.text.find('"err":1')
               if out is not -1:
                  print("Re Login")
                  mysession = login(user,password)
                  print("Login Sucess")
           time.sleep(300)
        sum=sum+1
    page=page+1
    submit_Nextpage(user,password,page,HEADERS,mysession,param2,n)


class A(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        submit(zh1,pa1,6,0)
        
class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        submit(zh2,pa2,7,0)
        
class C(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        submit(zh3,pa3,8,0)

class D(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        submit(zh4,pa4,9,0)
        
class E(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        submit(zh5,pa5,6,0)

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


