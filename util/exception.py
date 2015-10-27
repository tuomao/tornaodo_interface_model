#coding=utf-8
'''
Created on 2015年5月28日
'''
from common.errors import BaseError
__author__ = 'chenjian'

class BaseException(Exception):
    '''
    异常类
    '''
    def __init__(self, code, **kwargs):
        '''
        Constructor
        '''
        self.code = code
        self.message = BaseError.get_message(code)
        self.ext = kwargs

class ParamException(BaseException):
    '''
    UFOException的一个特例
    '''
    
    def __init__(self, name, **kwargs):
        '''
        '''
        
        BaseException.__init__(self, BaseError.ERROR_COMMON_REQUEST_PARAM_INVALID, **kwargs)
        
        self.message = '参数缺失或非法:' + name

class DBException(Exception):
    '''
    数据库异常类, 该异常属于底层数据库操作异常, 和业务逻辑无关.
    在业务层(processor)中捕获该异常后需要转化为UFOException
    '''

    