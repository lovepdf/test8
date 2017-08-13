# coding=utf-8
from django.db import models
from db.base_model import BaseModel
from db.base_manager import BaseModelManager
from utils.get_hash import get_hash

# Create your models here.

class PassportManager(BaseModelManager):
    def add_one_passport(self, username,password,email):
        '''
        添加一个账户信息
        '''
        obj = self.create_one_object(username=username,password=get_hash(password),email=email)
        return obj

    def get_one_passport(self,username,password=None):
        '''
        根据用户名和密码查询账户信息
        '''
        '''
        if password:
            obj = self.get_one_object(username=username,password=get_hash(password))
        else:
            obj = self.get_one_object(username=username)
        '''
        if password is None:
            obj = self.get_one_object(username=username)
        else:
            obj = self.get_one_object(username=username,password=get_hash(password))
        return obj

class Passport(BaseModel):
    '''
    用户账户类
    '''
    username = models.CharField(max_length=20,help_text='用户名')
    password = models.CharField(max_length=40, help_text='密码')
    email = models.EmailField(help_text='邮箱')

    # 创建一个自定义模型管理器的对象
    objects = PassportManager()

    class Meta:
        db_table = 's_user_account' # 指定表名


class AddressManger(BaseModelManager):
    '''
    地址模型管理器类
    '''
    def get_default_address(self, passport_id):
        '''
        查找账户的默认地址信息
        '''
        addr = self.get_one_object(passport_id=passport_id, is_default=True)
        return addr

    def add_one_address(self, passport_id, recipicent_name, recipicent_addr, recipicent_phone,zip_code):
        '''
        添加一个地址信息
        '''
        # 查找当前用户是否有默认地址
        addr = self.get_default_address(passport_id=passport_id)
        if addr:
            # 有默认地址
            addr = self.create_one_object(passport_id=passport_id,
                                          recipicent_name=recipicent_name,
                                          recipicent_addr=recipicent_addr,
                                          recipicent_phone=recipicent_phone,
                                          zip_code=zip_code)
        else:
            # 没有默认地址
            addr = self.create_one_object(passport_id=passport_id,
                                          recipicent_name=recipicent_name,
                                          recipicent_addr=recipicent_addr,
                                          recipicent_phone=recipicent_phone,
                                          zip_code=zip_code,
                                          is_default=True)
        return addr


class Address(BaseModel):
    '''
    地址类
    '''
    passport = models.ForeignKey('Passport', help_text='所属账户')
    recipicent_name = models.CharField(max_length=20, help_text='收件人')
    recipicent_addr = models.CharField(max_length=256, help_text='收件地址')
    recipicent_phone = models.CharField(max_length=11, help_text='联系电话')
    zip_code = models.CharField(max_length=6, null=True, blank=True, help_text='邮编')
    is_default = models.BooleanField(default=False, help_text='是否默认')

    objects = AddressManger()

    class Meta:
        db_table = 's_user_address'