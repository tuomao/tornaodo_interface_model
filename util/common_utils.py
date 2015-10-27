# coding=utf-8
'''
Created on 2015年5月28日
'''
import datetime
import json
from bson.objectid import ObjectId
import sys
import traceback
import time
import torndb
from hashlib import md5, sha1
__author__ = 'chenjian'

class ComplexEncoder(json.JSONEncoder):
    '''
    encoder for json dumps
    '''
    
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, ObjectId):
            return obj.__str__()
        else:
            return json.JSONEncoder.default(self, obj)

def trace_error():
    '''
    trace exception info, output in sys.stdout
    '''
    
    etype, evalue, tracebackObj = sys.exc_info()[:3]
    print("Type: " , etype)
    print("Value: " , evalue)
    traceback.print_tb(tracebackObj)
    
def currentframe():
    '''
    Return the frame object for the caller's stack frame.
    '''
    
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back

if hasattr(sys, '_getframe'): currentframe = lambda: sys._getframe(3)

def str_to_datetime(string, formate='%Y-%m-%d'):
    date_time = datetime.datetime.strptime(string, formate)
    return date_time

# #
# @brief 将datetime转化为str
# @param formate 要转化的str的格式，默认为%Y-%m-%d
def datetime_to_str(datetime, formate='%Y-%m-%d'):
    return datetime.strftime(formate)

# #
# @brief 将datetime转化为时间戳
#
def datetime_to_timetuple(date_time):
    time.mktime(date_time.timetuple())

# #
# @brief 将时间戳转化为str
#
def timetuple_to_str(timetuple, formate='%Y-%m-%d'):
    time.strftime(formate, time.localtime(timetuple))
    
def request_to_dict(request):
    '''
    将x-www-form-urlencoded形式的参数转化为dict
    '''
    
    arguments = {}
    map(lambda name: arguments.setdefault(name, request.arguments[name][0] if len(request.arguments[name]) == 1 else request.arguments[name]), request.arguments)
    
    return arguments

def is_web_request(user_agent):
    '''
    通过user_agent判断是否是web请求
    '''
    
    platforms = ['iPod', 'iPhone', 'iPad', 'Android']
    
    for item in platforms:
        if item in user_agent:
            return False
    
    return True

##
# @brief 将对象实例转化为dict
# @param obj 对象的实例
#
#
def object2dict(obj):
    #convert object to a dict
    d = {}
    d['__class__'] = obj.__class__.__name__
    d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d


###
#@brief 将dict转化为对象
#@param d dict的对象
#
def dict2object(d):
    #convert dict to object
    if'__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module,class_name)
        args = dict((key.encode('ascii'), value) for key, value in d.items()) #get args
        inst = class_(**args) #create new instance
    else:
        inst = d
    return inst

class TornDBConnector(object):
    '''
    简单的torndb操作类, 用于单独建立和销毁数据库连接
    '''
    
    def __init__(self, **settings):
        self.conn = torndb.Connection(**settings)
        
    def __enter__(self):
        '''
        '''
        return self.conn
        
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
        
    def __del__(self):
        if self.conn:
            self.conn.close()