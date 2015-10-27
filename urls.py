#coding=utf-8
from handler.main_handler import MainHandler

__author__ = 'tuomao'

# handler路由
handlers = [
    # 请求主handler
    (r'/v1/?', MainHandler),
]

# 协议号和processor的映射
processor_mapping = {}

def processor(cmdid, is_internal=False):
    '''
    装饰器, 用于装饰processor中的主类
            作用是建立协议号和主类的映射
    '''
    def _module_dec(cls):
        processor_mapping[cmdid] = cls, is_internal
        return cls
    return _module_dec
