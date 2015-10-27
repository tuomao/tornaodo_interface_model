#coding=utf-8
__author__ = 'tataufo'

class BaseConstant(object):
    # 关闭server的时候，最长等待的时间
    MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 5

    #协议号
    CMD_LOGIN = 1
    # 获取用户的姓名
    CMD_GET_USERNAME =2