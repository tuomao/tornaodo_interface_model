#coding=utf-8
import logging
import sys
import json
import os

__author__ = 'tuomao'

if hasattr(sys, 'frozen'):
    _srcfile = "util%slogging_utils%s" % (os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

class Tracker(object):
    '''
    log tracker, to record things happened in one HTTP request 
    '''
    
    def __init__(self, logger='track'):
        '''
        '''
        
        self.logger = logging.getLogger(logger)
        # 因为这里封装了logger, 所以记录日志时查找上一帧的时候会找到本类中的方法, 导致无法正确记录调用者的file, func和lineno
        # 此处修正这个问题
        self.logger.findCaller = self._findCaller

    def logging_request_header(self, handler):
        '''
        append record request header in log file
        '''
    
        try:
            header_msg = json.dumps(handler.request.headers).decode('unicode_escape')
            self.logger.debug(self._assemble_msg('RequestHeader', header_msg))
        except:
            self.trace_error()
        
    def logging_request_body(self, handler):
        '''
        record request header in log file
        '''
        
        try:
            # TODO: if protocol buffer is used, body_msg has to change
            body_msg = handler.request.body.decode('unicode_escape').replace('\n', '')
            self.logger.debug(self._assemble_msg('RequestBody', body_msg))
        except:
            self.trace_error()
        
    def logging_response(self, handler):
        '''
        record response in log file
        '''
        
        try:
            response_msg = json.dumps(handler.res).decode('unicode_escape')
            self.logger.debug(self._assemble_msg('ResponseMsg', response_msg))
        except:
            self.trace_error()
            
    def _assemble_msg(self, msg_tag, msg_body):
            '''
            组织消息体
                
            Args:
                msg_tag : 消息标识
                msg_body ：消息体
            '''
        
            # format : tag:msg_body
            return '%s:%s' % (msg_tag, msg_body)
        
    def trace_error(self, tag=''):
        '''
        record exception stack in log file
        '''
        
        string = '%s:%s\nType: %s\nValue: %s' if tag else '%s%s\nType: %s\nValue: %s'
        
        etype, evalue, tracebackObj = sys.exc_info()[:3]
        self.logger.exception(string %(tag, "ErrorStack:", etype, evalue))
    
    def info(self, msg, tag=''):
        '''
        info
        '''
        
        if tag:
            self.logger.info('%s:%s'% (tag, msg))
        else:
            self.logger.info(msg)
    
    def debug(self, msg, tag=''):
        '''
        debug
        '''
        
        if tag:
            self.logger.debug('%s:%s'% (tag, msg))
        else:
            self.logger.debug(msg)
    
    def error(self, msg, tag=''):
        '''
        error
        '''
        
        if tag:
            self.logger.error('%s:%s'% (tag, msg))
        else:
            self.logger.error(msg)
    
    def warn(self, msg, tag=''):
        '''
        warning
        '''
        
        if tag:
            self.logger.warn('%s:%s'% (tag, msg))
        else:
            self.logger.warn(msg)
            
    def exception(self, e, tag=''):
        '''
        exception stack
        '''
        
        self.logger.exception(e)
            
    def _findCaller(self):
        '''
        获取调用者信息, 用于记录file func lineno
        '''
        
        f = logging.currentframe()

        if f is not None:
            f = f.f_back.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv
