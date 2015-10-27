#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015-4-21

@author: abel
'''
import codecs
import socket
import os
import database_setting
import sys

# 避免 utf-8mb4的错误
# from tornado.options import options
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)
#设置sys的默认编码是utf-8
reload(sys)
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

# 生产环境IP
PRODUCT_HOSTS =['192.168.56.1']
# 测试环境IP
TEST_HOSTS = ['192.168.56.1']

# 本机IP
LOCAL_HOST = socket.gethostbyname(socket.gethostname())
print  LOCAL_HOST

LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')


# 根据不同环境而不同的配置
# Product environment
if LOCAL_HOST in  PRODUCT_HOSTS:

    # 日志目录
    LOG_DIR = '/mnt/imc_logs'
    # 数据库配置
    DATABASE = database_setting.RELEASE

else:
    # 非正式环境
    if LOCAL_HOST in TEST_HOSTS:
        # 测试环境
        SMS_CHINA_URL = 'http://www.tataufo.com'
        SMS_OVERSEA_URL = 'http://www.tataufo.com'
        SERVER_NAME = 'test.tataufo.com'
        NOTIFICATION_SERVER = 'http://test.tataufo.com:3000/message/create/'
        FEED_SERVER='http://feed00.tataufo.com'
        SIG_SERVER = 'http://test.tataufo.com:16000'
        DATABASE = database_setting.TEST
        SMS_DEBUG_SWITCH = True
    else:
        print 'current host is not in test hosts or release hosts'

