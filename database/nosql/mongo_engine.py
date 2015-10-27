#coding=utf-8
'''
Created on 2015年5月28日
'''
__author__ = 'chenjian'

class MongoEngine(object):
    '''
    mongodb operation
    '''

    def __init__(self, conn_write, conn_read, tracker=None):
        self._conn_write = conn_write
        self._conn_read = conn_read
        self._tracker = tracker
        
    def save(self, db_name, table_name, data):
        '''
        MongoDB插入方法
        Args:
            db_name: str, 数据库名称
            table_name: str, 表名
            data: dict, 插入数据
        Return:
            ObjectId
        '''
        
        return self.get_table(db_name, table_name).insert(data)
    
    def update(self, db_name, table_name, condition, data, upsert=False, multi=True):
        '''
        MongoDB更新方法
        Args:
            db_name: str, 数据库名称
            table_name: str, 表名
            condition: dict, 条件
            data: dict, 更新数据
            upsert: boolean, 如果记录已经存在，更新它，否则新增一个记录, 默认为False
            multi：boolean, 如果有多个符合条件的记录，是否全部更新, 默认为True
        '''
        
        return self.get_table(db_name, table_name).update(condition, data, upsert=upsert, multi=multi)
    
    def query(self, db_name, table_name, condition, fields=None, order_by=None, skip=None, limit=None, is_count=False):
        '''
        MongoDB查询方法
        Args:
            db_name: str, 数据库名称
            table_name: str, 表名
            condition: dict, 条件
            fields: dict, 查询字段, False代表不查询此字段, True代表查询此字段
            order_by: list, 排序条件, 元素为元组, 元组第一个元素为排序字段, 第二个元素为正序/倒序, 1代表正序, 0代表倒序
            skip: int, 分页起始位置, 0代表从第一条开始, 不传limit代表从第n条之后的数据
            limit: int, 分页查询个数, 不传skip则从第一条开始
            is_count: boolean, 是否是返回count
        '''
        
        table = self.get_table(db_name, table_name, True)
        result = table.find(condition, fields)
        
        if order_by is not None:
            result = result.sort(order_by)
        if skip is not None:
            result = result.skip(skip)
        if limit is not None:
            result = result.limit(limit)
        if is_count:
            result = result.count()
        return result
    
    def delete(self, db_name, table_name, condition):
        '''
        MongoDB删除方法
        Args:
            db_name: str, 数据库名称
            table_name: str, 表名
            condition: dict, 条件
        '''
        
        return self.get_table(db_name, table_name).remove(condition)
    
    def query_one(self, db_name, table_name, condition, fields={'_id':False}):
        '''
        MongoDB查询一条记录
        Args:
            db_name: str, 数据库名称
            table_name: str, 表名
            condition: dict, 条件
            fields: dict, 查询字段, False代表不查询此字段, True代表查询此字段
        '''
        
        return self.get_table(db_name, table_name, True).find_one(condition, fields)
        
    def get_table(self, db_name, table_name, is_read=False):
        '''
        根据数据库名称和表名获取mongo的表
        '''
        
        if is_read:
            return self._conn_read[db_name][table_name]
        else:
            return self._conn_write[db_name][table_name]
    
    def drop(self, db_name, table_name):
        '''
        删除一张表
        '''
        self._conn_write[db_name][table_name].drop()