#coding=utf-8
'''
Created on 2015年6月4日
'''
import urllib
import urllib2
import setting
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
import json
import jpush
import urllib

__author__ = 'chenjian'

class PushService(object):
    '''
    '''
    
    def __init__(self, processor):
        '''
        '''
        
        self._processor = processor

    def push(self, data, *targets):
        '''
        jpush通知
        :param targets: 列表, 推送目标 []
        :param data: 字典, 推送数据
        '''
        
        try:
            try:
                _jpush = jpush.JPush(*setting.JPUSH['auth'])
                self._push(_jpush, targets, data)
            except:
                # 调用auth_new来发送(google版)
                _jpush = jpush.JPush(*setting.JPUSH['auth_google'])
                self._push(_jpush, targets, data)
        except:
            self._processor.tracker.trace_error()


    def _push(self, _jpush, targets, data):
        '''
        '''
        targets = [str(target) for target in targets]
        # TODO: 测试环境写成愿愿的id
#         targets = ["341255"]
        push = _jpush.create_push()
        push.audience = jpush.audience(
                            jpush.tag(*targets)
                        )
        push.notification = jpush.notification(alert=data['content'],
                                               ios=jpush.ios(alert=data['content'], badge=1, sound='default', extras=data['extras']),
                                               android=jpush.android(alert=data['content'], extras=data['extras'])
                                               )
        push.options = jpush.options({'sendno': 123456, 'apns_production': True, 'big_push_duration': 0})
        push.platform = jpush.all_
        push.send() 
    
    def notify(self, source, target_userid, data):
        '''
        站内信通知
        :param source:
        :param target_userid: 目标用户id
        :param data:
        :return:
        '''
        def _on_response(response):
            pass
        client = AsyncHTTPClient()
        self._processor.tracker.info(urllib.urlencode(data))

        request = HTTPRequest('%s?source=%s&userid=%s'% (setting.NOTIFICATION_SERVER, source, target_userid), method='POST', body=urllib.urlencode(data))
        client.fetch(request, callback=_on_response)