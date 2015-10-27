#coding=utf-8
'''
Created on 2015年5月27日
'''
import time

import setting
from database.nosql.mongo_engine import MongoEngine
from  database.rdbs.tataufo import TestDB
__author__ = 'chenjian'

class BaseProcessor(object):
    '''
    classdocs
    '''
    def __init__(self, handler):
        '''
        Constructor
        '''
        self.handler = handler
        self.application = handler.application
        self.params = handler.params
        self.cmdid = handler.cmdid
        self.userid = handler.userid
        self.userkey = handler.userkey
        self.timestamp = handler.timestamp
        
        # 当前时间戳(秒)
        self.NTIME = int(time.time())

        # logger
        self.tracker = handler.tracker
        self.sys_logger = handler.sys_logger
        
        # databases
        db_conns = self.application.db_conns

        self.testdb = TestDB(db_conns['test_read'], db_conns['test_write'])

        # 参数校验
        self._verify_params()

    def _verify_params(self):
        '''
        to be override if needed
        '''