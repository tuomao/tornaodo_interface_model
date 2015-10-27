#coding=utf-8
'''
Created on 2015年5月28日
'''
import json
from common.errors import BaseError
from util.common_utils import ComplexEncoder
__author__ = 'chenjian'

class ResponseBuilder(object):
    '''
    响应
    '''

    @staticmethod
    def build_error(handler, e):
        '''
        返回错误
        
        Args:
            handler: torndb.web.RequestHandler object
            e: An instance of UFOException
        Returns:
            A json string
        '''
        
        res = {}
        res['code'] = e.code
        res['message'] = e.message
        res['timestamp'] = handler.timestamp
        res['cmdid'] = handler.cmdid
        res.update(e.ext)
        
        return res
    
    @staticmethod
    def build_success(handler, data=None):
        '''
        返回成功
        
        Args:
            handler: torndb.web.RequestHandler object
            data: data returned by processor     
        Returns:
            A json string
        '''
        
        res = {}
        res['code'] = BaseError.SUCCESS
        res['message'] = BaseError.get_message(res['code'])
        res['timestamp'] = handler.timestamp
        res['cmdid'] = handler.cmdid
        res['data'] = data if data is not None else {}
        
        return res