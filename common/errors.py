# coding=utf-8
from common.common_errors import CommonError
__author__ = 'tuomao'

class BaseError(CommonError):
    '''
    本模块从11001-11999
    为了防止错误码重复, 按人分配区域
    cj: 1-200
    shenhong: 200-400
    yuheng: 400-600
    yuanyuan: 600-800
    chenliang: 800-999
    '''

    
    # code

    ERROR_RONG_REQUEST_ERROR=11201


    # message
    message = {
        ERROR_RONG_REQUEST_ERROR:'融云请求错误'
    }
    message.update(CommonError.common_message)
    
    
    @staticmethod
    def get_message(code):
        return BaseError.message.get(code)
