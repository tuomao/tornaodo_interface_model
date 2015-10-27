#coding=utf-8
'''
Created on 2015年6月18日
'''
from tornado import gen

from common.constants import BaseConstant
import urls
from processor.base_processor import BaseProcessor

__author__ = 'chenjian'

@urls.processor(BaseConstant.CMD_GET_USERNAME)
class GetUserName(BaseProcessor):
    '''
    获取GetUserName
    '''
    
    TAG = 'GetUserName'
    
    def __init__(self, handler):
        '''
        Constructor
        '''
        BaseProcessor.__init__(self, handler)
        
        # define member variables here

    @gen.coroutine
    def process(self):
        '''
        process protocol
        '''

        name = self.testdb.get_name_by_id(self.params['id'])

        return_data = name
        return return_data
        
    def _verify_params(self):
        '''
        重写父类方法, 作参数校验
        '''
        
