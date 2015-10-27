#coding=utf-8
__author__ = 'tuomao'
##@brief 对象和dict之间转换的工具类

##
# @brief 将对象实例转化为dict
# @param obj 对象的实例
#
#
def object2dict(obj):
    #convert object to a dict
    d = {}
    d['__class__'] = obj.__class__.__name__
    d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d


###
#@brief 将dict转化为对象
#@param d dict的对象
#
def dict2object(d):
    #convert dict to object
    if'__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module,class_name)
        args = dict((key.encode('ascii'), value) for key, value in d.items()) #get args
        inst = class_(**args) #create new instance
    else:
        inst = d
    return inst