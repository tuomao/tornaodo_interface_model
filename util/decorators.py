#coding=utf-8
'''
Created on 2015年5月28日
'''
from util.exception import BaseException, DBException
from common.errors import BaseError
from functools import wraps
from common.constants import BaseConstant

import sys
__author__ = 'chenjian'

def user_auth(func):
    '''
    用于修饰processor类中的process方法, 做userid和private_key的匹配校验
    '''
    
    @wraps(func)
    def _dec(*args, **kwargs):
        processor = args[0]
        userid = processor.userid
        key = processor.userkey

        return func(*args, **kwargs)
    return _dec
        
def singleton(cls):  
    '''
    单例模式装饰器, 被装饰的类将成为单例类
    '''
    instances = {}  
    @wraps(cls)
    def _singleton(*args, **kw): 
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton

def db_operator(func):
    '''
    用于修饰数据库操作类(如BaseDB)中的方法, 将异常转化为DBException
    '''
    @wraps(func)
    def _dec(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e:
            # 为了保留原异常栈信息, 需要同时raise traceback对象
            raise DBException, DBException(e), sys.exc_info()[2]
    return _dec

def deprecated(o):
    '''
        class or function to be deprecated
    :raise: Exception
    '''

    # raise DeprecationWarning
    raise Exception("Deprecated class or function:" + o.__name__)