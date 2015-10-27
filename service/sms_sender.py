# coding=utf-8
'''
Created on 2015年6月3日
'''
import requests
import time
import setting


class SmsSender(object):
    """
    短信发送类
    smstype 发送类型，1为国内注册验证码，2为hey，3为like, 4为like_reply, 5为国内语音验证, 6为国内或国外普通模式, 7为oversea注册验证码, 8为oversea语音验证
    action 普通短信为'sms', 'voice'为语音短信
    prefix 手机号前缀, 国内短信可以不传, 或者传'+86', 国外短信需要传否则会发送失败.
    content 发送内容, 不需要加任何类似"[tataUFO]"的后缀
    mobile 接收手机号, 纯手机号不要添加前缀
    必要的话可以继承此类实现自己的短信类
    """
    
    TYPE_CN_REGISTER_VERIFY = 1
    TYPE_SEND_HEY = 2
    TYPE_SEND_LIKE = 3
    TYPE_REPLY_LIKE = 4
    TYPE_CN_REGISTER_VOICE_VERIFY = 5
    TYPE_NORMAL = 6
    TYPE_OVERSEA_REGISTER_VERIFY = 7
    TYPE_OVERSEA_REGISTER_VOICE_VERIFY = 8
    
    ACTION_SMS = 'sms'
    ACTION_VOICE = 'voice'
    
    PREFIX_DEFAULT = '+86'

    def __init__(self, processor):
        self.china_url = setting.SMS_CHINA_URL
        self.oversea_url = setting.SMS_OVERSEA_URL
        self.tatadb = processor.tatadb

    def send_sms(self, mobile, content, smstype=None, prefix=None, action='sms'):
        if action == SmsSender.ACTION_SMS:
            self._send_sms(mobile, content, smstype, prefix)
        else:
            self._send_sms_voice(mobile, content, smstype, prefix)

    def _send_sms(self, mobile, content, smstype, prefix=None):
        if not prefix or prefix == SmsSender.PREFIX_DEFAULT:
            self._china_nomal(mobile, content, smstype)
        else:
            if prefix:
                mobile = prefix+mobile
            self._oversea_nomal(mobile, content, smstype)

    def _send_sms_voice(self, mobile, content, smstype, prefix=None):
        if not prefix or prefix == SmsSender.PREFIX_DEFAULT:
            self._china_voice(mobile, content, smstype)
        else:
            if prefix:
                mobile = prefix+mobile
            self._oversea_voice(mobile, content, smstype)

    def _china_nomal(self, mobile, content, smstype):
        data = dict(
            phone = mobile,
            content = content,
            type = smstype
        )
        self._serder(self.china_url, data)

    def _oversea_nomal(self, mobile, content, smstype):
        data = dict(
            phone = mobile,
            content = content,
            type = smstype
        )
        self._serder(self.oversea_url, data)

    def _china_voice(self, mobile, content, smstype):
        data = dict(
            phone = mobile,
            content = content,
            type = smstype if smstype else SmsSender.TYPE_CN_REGISTER_VOICE_VERIFY
        )
        self._serder(self.china_url, data)

    def _oversea_voice(self, mobile, content, smstype):
        data = dict(
            phone = mobile,
            content = content,
            type = smstype if smstype else SmsSender.TYPE_OVERSEA_REGISTER_VOICE_VERIFY
        )
        self._serder(self.oversea_url, data)

    def _serder(self, url, data):
        return requests.post(url, data)

    def check_verify_code(self, mobile, code):
        '''
        校验验证码
        '''

        condition = {}
        condition['code'] = code
        condition['mobile'] = mobile
        # do we need an enum type here?
        condition['verified'] = 0

        update_data = {}
        update_data['verified'] = 1

        result = self.tatadb.update_by_condition('verification_codes', update_data, condition)

        return True if result else False
    
    def is_verified(self, mobile, code):
        '''
        检查是否已经验证通过
        '''

        condition = {}
        condition['code'] = code
        condition['mobile'] = mobile
        condition['verified'] = 1

        result = self.tatadb.query_by_condition('verification_codes', ('verified', ), condition)

        return True if result else False
    
    def add_verify_code(self, mobile, code):
        """
        添加验证码
        :param mobile:
        :param code:
        :return:
        """
        data = {'mobile':mobile, 'code':code, 'verified':0, 'sent_at':int(time.time())}
        self.tatadb.save('verification_codes',data)
