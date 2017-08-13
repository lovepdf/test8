# coding=utf-8
from hashlib import sha1


def get_hash(str, salt=None):
    '''
    获取一个字符串的哈系值
    '''
    str = '!@#$%' + str + '@$$!@@'
    if salt:
        str = str + salt
    sh = sha1()
    sh.update(str)
    return sh.hexdigest()