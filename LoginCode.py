#!/usr/bin/python 
# -*- coding: utf-8 -*-

import numpy as np
import shutil
import tensorflow as tf
import cv2
import os
import random
import time
import sys
import socket
import struct
import requests
import re
import threading


class LoginCode:
    """docstring for Login"""

    def __init__(self):
        super(LoginCode, self).__init__()
        self.output = self.crack_captcha_cnn()
        self.saver = tf.train.Saver()
        with tf.Session().as_default() as sess:
            self.sess = sess
            self.saver.restore(self.sess, tf.train.latest_checkpoint(self.model_path))
            self.predict = tf.argmax(tf.reshape(self.output, [-1, self.MAX_CAPTCHA, self.CHAR_SET_LEN]), 2)
    
    CHAR_SET = ['c', 'l', 'o', 'k', 'p', 'e', 't', 'u', 'v', 'b', 'j', 'm', 'z', 'g', 'w', 'f', 's', 'n', 'x', 'i', 'q', 'd', 'r', 'y', 'a', 'h']
    # 图像大小
    IMAGE_HEIGHT = 30
    IMAGE_WIDTH = 70
    MAX_CAPTCHA = 4
    CHAR_SET_LEN = len(CHAR_SET)
    model_path = './VerifyCode/Model/'
    image_path = './VerifyCode/Info/'
    X = tf.placeholder(tf.float32, [None, IMAGE_HEIGHT * IMAGE_WIDTH])
    Y = tf.placeholder(tf.float32, [None, MAX_CAPTCHA * CHAR_SET_LEN])
    keep_prob = tf.placeholder(tf.float32)  # dropout

    HEADERS = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Referer': 'http://sns.qnzs.youth.cn/',
        'X-FORWARDED-FOR':'',
        'X-Requested-With':'XMLHttpRequest',
        'CLIENT-IP':''
            }
     
    # 定义CNN
    def crack_captcha_cnn(self,w_alpha=0.07, b_alpha=0.03):
        x = tf.reshape(self.X, shape=[-1, self.IMAGE_HEIGHT, self.IMAGE_WIDTH, 1])
     
        # 3 conv layer
        w_c1 = tf.Variable(w_alpha * tf.random_normal([3, 3, 1, 32]))
        b_c1 = tf.Variable(b_alpha * tf.random_normal([32]))
        conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, w_c1, strides=[1, 1, 1, 1], padding='SAME'), b_c1))
        conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        conv1 = tf.nn.dropout(conv1, self.keep_prob)
     
        w_c2 = tf.Variable(w_alpha * tf.random_normal([3, 3, 32, 64]))
        b_c2 = tf.Variable(b_alpha * tf.random_normal([64]))
        conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, w_c2, strides=[1, 1, 1, 1], padding='SAME'), b_c2))
        conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        conv2 = tf.nn.dropout(conv2, self.keep_prob)
     
        w_c3 = tf.Variable(w_alpha * tf.random_normal([3, 3, 64, 64]))
        b_c3 = tf.Variable(b_alpha * tf.random_normal([64]))
        conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, w_c3, strides=[1, 1, 1, 1], padding='SAME'), b_c3))
        conv3 = tf.nn.max_pool(conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        conv3 = tf.nn.dropout(conv3, self.keep_prob)
     
        # Fully connected layer
        w_d = tf.Variable(w_alpha * tf.random_normal([4 * 9 * 64, 1024]))
        b_d = tf.Variable(b_alpha * tf.random_normal([1024]))
        dense = tf.reshape(conv3, [-1, w_d.get_shape().as_list()[0]])
        dense = tf.nn.relu(tf.add(tf.matmul(dense, w_d), b_d))
        dense = tf.nn.dropout(dense, self.keep_prob)
     
        w_out = tf.Variable(w_alpha * tf.random_normal([1024, self.MAX_CAPTCHA * self.CHAR_SET_LEN]))
        b_out = tf.Variable(b_alpha * tf.random_normal([self.MAX_CAPTCHA * self.CHAR_SET_LEN]))
        out = tf.add(tf.matmul(dense, w_out), b_out)
        # out = tf.nn.softmax(out)
        return out
     
     
    # 向量转回文本
    def vec2text(self,vec):
        char_pos = vec.nonzero()[0]
        text = []
        for i, c in enumerate(char_pos):
            char_at_pos = i  # c/63
            char_idx = c % 26
            char_code = char_idx + ord('a')
            text.append(chr(char_code))
        return "".join(text)
     
     
    def CodeMatch(self,user):
        image_p = os.path.join(self.image_path, str(user) + ".png")
        # 单张图片预测
        image = np.float32(cv2.imread(image_p, 0))
        image = image.flatten() / 255
 
        text_list = self.sess.run(self.predict, feed_dict={self.X: [image], self.keep_prob: 1})
 
        text = text_list[0].tolist()
        vector = np.zeros(self.MAX_CAPTCHA * self.CHAR_SET_LEN)
        i = 0
        for n in text:
            vector[i * self.CHAR_SET_LEN + n] = 1
            i += 1
        # print(vector)
        predict_text= self.vec2text(vector)
        print(predict_text)
        return predict_text


    def GetCode(self,user,password):
        count = 0
        success = 0
        while True:
            count+=1
            print(count,end = " ")
            IP = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
            self.HEADERS['X-FORWARDED-FOR'] = IP
            self.HEADERS['CLIENT-IP'] = IP
            mysession = requests.Session()
            login_url = 'http://sns.qnzs.youth.cn/index/index'
            html = mysession.post(login_url,timeout=60*4 , headers=self.HEADERS)
            regx=r'/index/captcha.[\S]*"'  
            pattern=re.compile(regx) 
            listurl=re.findall(pattern,repr(html.text)) 
            if not len(listurl) :
                continue
            url2='http://sns.qnzs.youth.cn'+listurl[0]
            checkcode = mysession.post(url2,timeout=60*4 ,headers=self.HEADERS)
            with open('./VerifyCode/Info/%s.png' % (user),'wb') as f:
                    f.write(checkcode.content)
            time.sleep(1)
            code = self.CodeMatch(user)
            param={
                    'user[mobile]':'13061330723','user[pwd]':'ZzM4ODlteHI=','user[code]':'1234','user[con]':'index','user[id]':'df7d771c'
                }
            param['user[mobile]']=user
            param['user[pwd]']=password
            param['user[code]']=code
            url4='http://sns.qnzs.youth.cn/ajax/login'
            html = mysession.post(url4,data=param, headers=self.HEADERS)
            #print(html.text)
            o = html.text.find('"err":6')
            if o is not -1:
                success += 1
                print("SUCCESS " + str(success) + " " + code)
                print("识别率" + " " + str(success / count))
                with open('./VerifyCode/Train/%s.png' % (code),'wb') as f:
                    f.write(checkcode.content)
            break


# v = LoginCode()
# class A(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         v.GetCode(1,1)

# if __name__ == '__main__':
#     t1 = A()
#     t1.start()