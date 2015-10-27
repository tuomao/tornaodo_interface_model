# coding=utf-8
'''
Created on 2013-11-13

@author: chenjian
'''

class RedisEngine(object):
    '''
    redis
    '''
    
    def __init__(self, conn_read, conn_write):
        self._conn_read = conn_read
        self._conn_write = conn_write
        
    def _repr_value(self, value):
        '''
        处理查询结果, 字符串decode为unicode, 'None'修改为None
        '''
        if not value:
            pass
        elif value == 'None':
            value = None
        else:
            value = value.decode('utf-8')
        
        return value
        
    def del_keys(self, *keys): 
        '''
        删除
                        
        Args:
            *keys:一个或多个key
        '''
        
        return self._conn_write.delete(*keys)  
        
    def set_expiration(self, key, expire_seconds):
        '''
        设置过期时间
        
        Args:
            key:键
            expire_seconds:需要设置的过期时间
        '''
        
        return self._conn_write.expire(key, expire_seconds)
        
    def get_hash(self, key):
        '''
        根据key查询缓存
                        
        Args:
            key:str类型redis中的键
        Returns:
            根据key查询到对应的hash类型数据,若不存在返回None
        '''
        
        data = self._conn_read.hgetall(key)
        # 字符串转化为unicode
        for item in data:
            data[item] = self._repr_value(data[item])
        return data if len(data) > 0 else None
    
    def upsert_hash_field_value(self, key, field, value):
        '''
        插入/更新 key值对应的hash数据的field--value数据
                         
        Args:
            key:键
            field:hash表中的字段名
            value:hash表中field对应的值
        '''

        return self._conn_write.hset(key, field, value)
        
    def get_hash_field_value(self, key, field):
        '''
        获取key值对应的hash数据的field对应的value,无则返回None
                        
        Args:
            key:键
            field:hash表中的字段名
        Returns:
            不存在hash表或者表中的field则返回None
            存在则返回field对应的value
        '''

        value = self._conn_read.hget(key, field)
        return self._repr_value(value)
    
    def get_hash_fields(self, key):
        '''
            获得指定key对应的hash存储类型中的所有字段,返回list,若没有则返回空list
                        
        Args:
            key:键
        Returns:
            返回list,若key不存在则返回空的list
        '''
        
        return self._conn_read.hkeys(key)
    
    def upsert_hash(self, key, data, expire_seconds=None):
        '''
        有则更新,无则新增
                        
        Args:
            key:键
            data:字典类型的数据
            expire_seconds:过期时间,不传则该hash表没有过期时间
        '''
        
        result = self._conn_write.hmset(key, data)
        if expire_seconds:
            self.set_expiration(key, expire_seconds)
        return result
        
    def get_string(self, key):
        '''
            获取单个key对应的string
                        
        Args:
            key: str类型
        Returns:
            返回key对应的字符串,若key不存在则返回None
        '''
        
        return self._repr_value(self._conn_read.get(key))
    
    def get_string_list(self, keys):
        '''
        获取多个key各自对应的数据
                        
        Args:
            keys:list,tuple,set类型都可以
        Returns:
            list类型,若有key不存在,对应的元素为None
        '''
        
        return map(self._repr_value, self._conn_read.mget(keys))
        
    def upsert_string(self, key, value, expire_seconds=None):
        '''
        一次插入/更新一条数据
                        
        Args:
            key:键
            value:键对应的字符串
            expire_seconds:过期时间,不传则该键没有过期时间
        '''
        
        result = 0
        # 设置生存时间
        if expire_seconds:
            result = self._conn_write.setex(key, expire_seconds, value)
        # 不设置生存时间
        else:
            result = self._conn_write.set(key, value)
        return result
    
    def upsert_string_batch(self, data):
        '''
        data is type of dict, 批量添加string类型数据
        
        Args:
            data: 字典类型,每一条键值分别是redis中的键和值
        '''

        return self._conn_write.mset(data)
        
    def exists_or_not(self, key):
        '''
        判断key是否存在
                        
        Args:
            key:键
        Returns:
           key存在则返回True,不存在则返回False
        '''
        
        return self._conn_read.exsits(key)
    
    def remove_expire_seconds(self, key):
        '''
        去掉过期时间
                        
        Args:
            key:键
        '''
        
        return self._conn_write.persist(key)
    
    def upsert_list(self, key, values):
        '''
        插入/更新 list
        Args:
            key: 键
            values: list
        '''
        
        pipe = self._conn_write.pipeline(transaction=False)
        for value in values:
            pipe.rpush(key, value)
            
        return pipe.execute()
    
    def get_list(self, key, start=0, end=-1):
        '''
        获取list
        Args:
            key: 键
            start: 起始索引
            end: 结束索引,start默认为0，end默认为-1,即默认获取整个list
        Return:
            list类型
        '''

        return map(self._repr_value, self._conn_read.lrange(key, start, end))
    
    def upsert_set(self, key, values):
        '''
        插入/更新 set
        Args:
            key: 键
            *values: list/set/tuple
        '''
        
        pipe = self._conn_write.pipeline(transaction=False)
        for value in values:
            pipe.sadd(key, value)
        
        result = pipe.execute()
        return result
    
    def get_set(self, key):
        '''
         获取set
        Args:
            key: 键
        Return:
            set类型
        '''
        
        results = set()
        map(lambda item: results.add(self._repr_value(item)), self._conn_read.smembers(key))
        return results
    
    def pipeline_upser(self, update_value):
        
        '''
        管道操作
        Args：
        Value ： 列表，其中的数据元素为元组类型；依次判断每个value中的每个元素，第一个元素为键，第二个元素为值；
                 当值为字符串、数字时等非结构化数据时定义为key-string的操作；当值为字典时定义为hash操作；
        '''
        if not isinstance(update_value, list):
            return
        
        pipe = self._conn_write.pipeline(transaction=False)
        for value in update_value:
            if isinstance(value[1], dict):
                # 字典做为hash处理
                pipe.hmset(value[0], value[1])
            elif isinstance(value[1], list) or isinstance(value[1], tuple):
                # 列表、元组处理
                for element in value[1]:
                    pipe.rpush(element)
            else:
                pipe.set(value[0], value[1])
        
        return pipe.execute()
    
        
    def left_push_list(self, key, *values):
        '''
        插入/更新list,每次在list开头添加一个值
        Args:
            key: 键
            value: 值
        '''
        
        return self._conn_write.lpush(key, *values)
    
    def rpop(self, key):
        '''
        弹出list队尾的一个值
        '''
        
        return self._conn_write.lpop(key)
    
    def left_trim_list(self, key, start, end):
        '''
        截断list,保存左边的值,保留的list中包括start和end索引
        Args:
            start: 起始索引
            end: 结束索引
        '''
        
        return self._conn_write.ltrim(key, start, end)
    
    def incr(self, key, amount=1):
        '''
        自增,只对字符串类型有效
        Args:
            key: 键名
            amount: 自增的
        Returns:
             自增后的数值
        '''
        
        return self._conn_write.incr(key, amount)
    
    def decr(self, key, amount=1):
        '''
        自减,只对字符串类型有效
        Args:
            key: 键名
            amount: 自减的值
        Returns:
            自减后的数值
        '''
        
        return self._conn_write.decr(key, amount)
    
    def get_keys(self, key_like=None):
        '''
         获取redis中键的数量,支持模糊查询
        Args:
            key_like: 模糊查询参数,不传则查询所有
        '''
        
        if key_like is None:
            return self._conn_read.keys()
        else:
            return self._conn_read.keys(key_like) 
        
    def del_hash_field(self, key, *fields):
        '''
        删除hash表中的字段
        Args:
            key: 键名
            *fields: 可变参数,字段名
        '''
        
        return self._conn_write.hdel(key, *fields)
    
    def del_from_set(self, key, *values):
        '''
        删除set中的指定元素
        Args:
            value: 要删除的元素
        '''
        
        return self._conn_write.srem(key, *values)
    
    def get_expire_time(self, key):
        '''
        查询redis中某个键的过期时间
        '''
        return self._conn_read.ttl(key)
    
