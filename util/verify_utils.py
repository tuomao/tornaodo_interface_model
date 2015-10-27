#coding=utf-8
'''
Created on 2013-10-28

@author: yangqing
'''
import re
import types
import time
try:
    from collections import OrderedDict
    ordereddict_available = True
except:
    ordereddict_available = False


def xss_filter(json_obj): 
    '''
    过滤非法字符
    '''
    if type(json_obj) is types.DictType:
        for item in json_obj:
            if xss_filter(json_obj[item]): 
                return True
    elif type(json_obj) is types.ListType:
        for item in json_obj:
            if xss_filter(item):
                return True
    else :
        str_json = str(json_obj)
        if '<' in str_json or '>' in str_json :           
            return True
        
    return False     

def is_int(var_obj):
    '''判断是否为32位整数'''
    return type(var_obj) is types.IntType# and var_obj >= -2147483648 and var_obj <= 2147483647 


def is_long(var_obj):
    '''判断是否为整数'''
    return type(var_obj) is types.LongType


def is_string(var_obj):
    '''判断是否为字符串 string'''
    return isinstance(var_obj, basestring)


def is_float(var_obj):
    '''判断是否为浮点数 1.324'''
    return type(var_obj) is types.FloatType


def is_dict(var_obj):
    '''判断是否为字典 {'a1':'1','a2':'2'}'''
    
    return type(var_obj) is types.DictType

def is_ordered_dict(var_obj):
    '''
    判断是否是有序字典
    '''
    if ordereddict_available:
        return isinstance(var_obj, OrderedDict)
    else:
        return False
    
def is_tuple(var_obj):
    '''判断是否为tuple [1,2,3]'''
    return type(var_obj) is types.TupleType

def is_list(var_obj):
    '''判断是否为List [1,3,4]'''
    return type(var_obj) is types.ListType

def is_boolean(var_obj):
    '''判断是否为布尔值 True'''
    return type(var_obj) is types.BooleanType

def is_datestring(time_str, time_format="%Y-%m-%d %H:%M:%S"):
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(time_str, time_format)
        return True
    except:
        return False
    
def is_email(var_obj):
    '''判断是否为邮件地址'''
    rule = '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
    match = re.match( rule , var_obj )

    if match:
        return True
    return False

    
def is_chinese_string(var_obj):
    '''判断是否为中文字符串'''
    for x in var_obj:
        if (x >= u"\u4e00" and x<=u"\u9fa5") or (x >= u'\u0041' and x<=u'\u005a') or (x >= u'\u0061' and x<=u'\u007a'):
            continue
        else:
            return False
    return True



def is_chinese_char(var_obj):
    '''判断是否为中文字符'''
    if var_obj[0] > chr(127):
        return True
    return False

def is_ip_addr(var_obj): 
    '''匹配IP地址'''
    rule = '\d+\.\d+\.\d+\.\d+'
    match = re.match( rule , var_obj )

    if match:
        return True
    return False    
    