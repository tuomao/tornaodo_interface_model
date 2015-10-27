#coding=utf-8
import logging
from util.decorators import db_operator

class BaseDB():
    '''
    关系型数据库基类, 提供增删改查的一些公用方法
    '''
    
    def __init__(self, conn_read, conn_write, tracker=None):
        self._conn_read = conn_read
        self._conn_write = conn_write
        self._tracker = tracker
    
    @db_operator
    def start_transaction(self):
        '''
                        开启事务
        '''
        self._conn_write.execute('BEGIN')
    
    @db_operator
    def commit(self):
        '''
                        提交事务
        '''
        self._conn_write.execute('COMMIT')
    
    @db_operator 
    def rollback(self):
        '''
                        回滚事务
        '''
        self._conn_write.execute('ROLLBACK')
    
    @db_operator
    def update(self, table_name, pk_entry, data={}, incr_data={}):
        '''
        根据主键更新 
            
        Args:
            table_name: 更新的表名
            pk_entry: 主键的键值,例如['txid',1]
            data: 参数字典,例如{'name':'zhangsan','age':12}
            upsert: 布尔型,True:则进行save_or_update操作.False:进行update操作
        Returns:
            execute row count
        '''
        items = ["update %s set "% (table_name)]
        for key in data:
            value = data.get(key)
            if  isinstance(value, (int,long,float)) or 'now()' == value:
                items.append("%s=%s,"% (key, value))
            else:
                items.append("%s='%s',"% (key, value))
        for key in incr_data: 
            value = incr_data.get(key)
            if value >= 0:
                items.append('%s=%s+%s,'% (key, key, value))
            else:
                items.append('%s=%s-%s,'% (key, key, -value))

        sql = ''.join(items)
        if isinstance(pk_entry[1], (int,long,float)):
            sql = sql[0:len(sql)-1] + " WHERE "+pk_entry[0]+"="+str(pk_entry[1])
        else:
            sql = sql[0:len(sql)-1] + " WHERE "+pk_entry[0]+"='"+str(pk_entry[1])+"'"
            
        return self._conn_write.execute_rowcount(sql) 
    
    @db_operator     
    def update_by_condition(self, table_name, data=None, condition_data=None, incr_data=None):
        '''
        根据条件更新 
            
        Args:
            table_name: 更新的表名
            condition_data: 查询条件数据,字典类型,例如{'name':'张三','age':13}
            data: 参数字典,例如{'name':'zhangsan','age':12}
            upsert: 布尔型,True:则进行save_or_update操作.False:进行update操作
        Returns:
        '''
        items = ["update %s set "% (table_name)]
        if data:
            for key in data:
                value = data.get(key)
                if  isinstance(value, (int,long,float)) or 'now()' == value:
                    items.append("%s=%s,"% (key, value))
                else:
                    items.append("%s='%s',"% (key, value))
        
        if incr_data:
            for key in incr_data: 
                value = incr_data.get(key)
                items.append('%s=%s+%s,'% (key, key, value))  
        sql = ''.join(items)
        
        # 拼' WHERE 1=1 AND xxx=xxx AND xxx like "%xx"'部分 
        if condition_data:
            condition_list = [" WHERE 1=1"]
            for key in condition_data:
                value = condition_data.get(key)
                if isinstance(value, (int,long,float)):
                    condition_list.append(" AND "+key+"=%s"% (value))
                elif isinstance(value, tuple):
                    dst_str = str(value)
                    condition_list.append(" AND "+key+" in %s"% (dst_str))
                else:
                    condition_list.append(" AND "+key+"='%s'"% (value))
            
            condition_str = ''.join(condition_list)
            sql = sql[0:len(sql)-1] + condition_str
        return self._conn_write.execute_rowcount(sql)

    @db_operator
    def get(self, table_name, fields, pk_entry, is_transaction=False):
        '''
        根据主键查询指定字段
                       
        Args:
            fields: 查询的字段,当需要起别名时可以传dict类型,不需要时可以传tuple,list,set类型
            pk_entry: 主键的键值,可以是list,tuple类型,例如['txid',1],('txid',1)
            data: 参数字典,例如{'name':'zhangsan','age':12}
            upsert: 布尔型,True:则进行save_or_update操作.False:进行update操作
        Returns:
            result: 如果有记录则返回该记录对应的字典
                                                            如果无记录则返回False
        '''
        items = ['SELECT ']
        if isinstance(fields, (tuple,list,set)):
            for field in fields:
                items.append(field+',')
        elif isinstance(fields, dict):
            for key in fields:
                items.append(key+' AS '+fields.get(key)+' ,')
        sql = ''.join(items)

        if isinstance(pk_entry[1], (int,float)):
            sql = sql[0:len(sql)-1] + " FROM " + table_name + " WHERE "+pk_entry[0]+"="+str(pk_entry[1])
        else:
            sql = "%s from %s where %s = '%s'"%(sql[0:len(sql)-1],  table_name, pk_entry[0], pk_entry[1])
            # sql = sql[0:len(sql)-1] + " FROM " + table_name + " WHERE "+pk_entry[0]+"='%s'"%pk_entry[1]
            
        if is_transaction:
            result = self._conn_write.query(sql)
        else:
            result = self._conn_read.query(sql)
        if (len(result)) > 0:
            return result[0]
        else:
            return None #代表无此记录,用于在module中判断并返回Errorcode.ERROR_NO_DATABASE_RECORD
        
    @db_operator
    def query_by_condition(self, table_name, fields=None, condition_data=None, orderby=None, limit=None, is_transaction=False):
        '''
        单表查询通用方法,支持指定查询字段,查询条件,模糊查询,排序查询
        
        Args:
            table_name: 查询的表名,字符串类型
            fields: 需要查询的字段,list类型,例如['name','age']
            condition_data: 查询条件数据,字典类型,例如{'name':'张三','age':13}
            fuzzy: condition_data中要模糊查询的键,list类型,例如需要 name like '%张%'时使用  ['name']
            orderby: 排序条件,列表,例如[('age', 'DESC'), ('id', 'ASC')]
            limit: 分页查询,元组,例如(0,1)
        Returns:
            result: list类型,其中的元素是字典类型
        '''
        
        # 拼'SELECT xx FRßOM xx'部分
        items = ['SELECT ']
        if not fields:
            items.append('*')
        else:
            for field in fields:
                items.append(field+',')
        sql_str = ''.join(items)
        sql_str = sql_str[0:len(sql_str)-1] + " FROM " + table_name 
        
        # 拼' WHERE 1=1 AND xxx=xxx AND xxx like "%xx"'部分 
        condition_str = ''
        if condition_data:
            condition_list = [" WHERE 1=1"]
            for key in condition_data:
                value = condition_data.get(key)
            
                if isinstance(value, (int,float)):
                    condition_list.append(" AND "+key+"=%s"% (value))
                elif isinstance(value, tuple):
                    dst_str = str(value)
                    condition_list.append(" AND "+key+" in %s"% (dst_str))
                else:
                    condition_list.append(" AND "+key+"='%s'"% (value))
            
            condition_str = ''.join(condition_list)
        
        # 拼' ORDER BY xx DESC,xx ASC' 部分
        orderby_str = ''    
        if orderby:
            order_list = []
            for item in orderby:
                order_list.append(item[0]+" "+ item[1])
            orderby_str = " ORDER BY " + ','.join(order_list)
        
        limit_str = ''    
        # 拼 ' limit ' 部分
        if isinstance(limit, int):
            limit_str = ' limit %s'% limit
        elif limit:
            if len(limit) == 1:
                limit_str = ' limit %s'% limit
            elif len(limit) == 2:
                limit_str = ' limit %s,%s'% limit
            
        # 拼接sql        
        sql = sql_str + condition_str + orderby_str + limit_str 
        if is_transaction:
            result = self._conn_write.query(sql)
        else:   
            result = self._conn_read.query(sql)
        return result
    
    @db_operator
    def batch_delete(self, table_name, pk_name, values=[]):
        '''
        批量删除
        '''
        sql = 'DELETE FROM ' + table_name + ' WHERE ' + pk_name + '=%s'
        self._conn_write.executemany(sql, values)
    
    @db_operator
    def delete_all(self, table_name):
        '''
        删除表中所有记录
        '''
        self._conn_write.execute('DELETE FROM %s'% (table_name))
    
    @db_operator
    def save(self, table_name, data):
        '''
        '''
        
        items = ["INSERT INTO %s("% (table_name)]
        values = ["VALUES("]
        for key in data:
            items.append('%s,'% (key))
            value = data.get(key)
            if  isinstance(value, (int,long,float)) or 'now()' == value:
                values.append("%s,"% (value))
            else:
                values.append("'%s',"% (value))
           
        items_str = ''.join(items)
        items_str = items_str[0:len(items_str)-1] + ') '
        values_str = ''.join(values)
        values_str = values_str[0:len(values_str)-1] + ')'
        sql = items_str + values_str
        return self._conn_write.execute_lastrowid(sql)
    
    @db_operator
    def delete(self, table_name, pk_entry):
        '''
        pk_entry: ('id', 2)
        '''
        
        sql = "DELETE FROM %s WHERE %s="
        if isinstance(pk_entry[1], (int,long,float)):
            sql += "%s"
        else:
            sql +="'%s'"
        sql = sql% (table_name, pk_entry[0], pk_entry[1])
        return self._conn_write.execute_lastrowid(sql)

    @db_operator     
    def delete_by_condition(self, table_name, condition_data=None):
        '''
        根据条件删除
            
        Args:
            table_name: 更新的表名
            condition_data: 查询条件数据,字典类型,例如{'name':'张三','age':13}
        Returns:
        '''
        
        assert condition_data, "Are you serious? The whole table will be delete!!!"
        
        sql = "delete from %s"% (table_name)
        
        # 拼' WHERE 1=1 AND xxx=xxx AND xxx like "%xx"'部分 
        condition_list = [" WHERE 1=1"]
        for key in condition_data:
            value = condition_data.get(key)
            if isinstance(value, (int,long,float)):
                condition_list.append(" AND "+key+"=%s"% (value))
            elif isinstance(value, tuple):
                dst_str = str(value)
                condition_list.append(" AND "+key+" in %s"% (dst_str))
            else:
                condition_list.append(" AND "+key+"='%s'"% (value))
        
        condition_str = ''.join(condition_list)
        sql += condition_str
            
        return self._conn_write.execute_rowcount(sql)