#coding=utf-8
'''
Created on 2015年5月27日
'''
import json

import tornado

from util.exception import BaseException, ParamException, DBException
import urls
from common.errors import BaseError
from util.protocol import ResponseBuilder
from util.common_utils import ComplexEncoder
from tornado import gen
from util import verify_utils


__author__ = 'chenjian'

class MainHandler(tornado.web.RequestHandler):
    '''
    main handler, receive requests and distribute them to processors
    '''
    
    def __init__(self, *request, **kwargs):
        '''
        Constructor
        '''
        
        super(MainHandler, self).__init__(request[0], request[1])
        self.set_header("Content-Type", "application/json")
        self.tracker = self.application.tracker
        self.sys_logger = self.application.sys_logger
        
        self.cmdid = 0
        self.timestamp = 0
        self.userid = None
        self.userkey = None
        self.params = dict()
        
        self.res = dict()
        
    def get(self):
        '''
        GET
        '''
        
        print('server is running...')
#         self.post()
        
    @tornado.web.asynchronous
    @gen.coroutine
    def post(self): 
        '''
        POST
        '''

        try:
            # 记录请求
            self.tracker.logging_request_header(self)
            # TODO: wait for protocol buffer
            self.tracker.logging_request_body(self)
            
            # 解析请求
            self._parse_request()
            
            # 分发processor
            processor = urls.processor_mapping.get(self.cmdid)
            if not processor:
                # 协议不存在
                raise BaseException(BaseError.ERROR_COMMON_CMD_NOT_EXISTS)
            
            # 协议处理
            if processor[1]:
                # 内部调用的协议
                raise BaseException(BaseError.ERROR_COMMON_PROTOCOL_FOR_INTERNAL_ONLY)
            processor = processor[0]
            data = yield processor(self).process()
            
            # 成功
            self.res = ResponseBuilder.build_success(self, data)
        except BaseException, e:
            # 根据捕获的UFOException返回错误信息
            self.res = ResponseBuilder.build_error(self, e)
        except DBException, e:
            # 如果是底层未处理的DBException, 在这里转化为UFOException
            self.tracker.trace_error()
            e = BaseException(BaseError.ERROR_COMMON_DATABASE_EXCEPTION)
            self.res = ResponseBuilder.build_error(self, e)
        except Exception, e:
            self.tracker.trace_error()
            e = BaseException(BaseError.ERROR_COMMON_UNKNOWN)
            self.res = ResponseBuilder.build_error(self, e)
        
        # 记录响应
        self.tracker.logging_response(self)
        
        # 响应
        self.write(json.dumps(self.res, cls=ComplexEncoder))
        self.finish()
        return
        
    def _parse_request(self):
        '''
        解析请求参数
        '''
        
        # 从header中解析参数
        try:
            self.cmdid = int(self.request.headers.get('cmdid', 0))
        except:
            raise ParamException('cmdid')
        
        try: 
            self.timestamp = long(self.request.headers.get('timestamp', 0))
        except:
            raise ParamException('timestamp') 
        
        # json解析 
        try:
            json_body = json.loads(self.request.body)
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)
        
        # TODO: 过滤非法字符
        
        # 参数校验
        self.userid = json_body.get('userid')
        if not verify_utils.is_int(self.userid):
            raise ParamException('userid')
        
        self.userkey = json_body.get('userkey')
        if not verify_utils.is_string(self.userkey):
            raise ParamException('userkey')
        
        self.params = json_body.get('params')
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')
        
    def _log(self):
        '''
        '''
        self.application.log_request(self)
