# coding=utf-8
'''
Created on 2015年5月28日
'''
from datetime import datetime
import time, random

from util.decorators import db_operator
from database.rdbs.base_db import BaseDB


__author__ = 'chenjian'


class TestDB(BaseDB):
    '''
    database: tataufo
    '''

    @db_operator
    def get_name_by_id(self, id):
        '''
        获取最新版本
        '''
        sql = 'select name from user WHERE id=%d' % (id)

        return self._conn_read.query(sql)[0]
