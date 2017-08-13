# coding=utf-8
from django.db import models
from db.base_model import BaseModel
from db.base_manager import BaseModelManager

# Create your models here.
from df_goods.models import Image


class OrderBasicLogicManager(BaseModelManager):
    '''
    订单基本模型逻辑管理类
    '''
    def get_order_list_by_passport(self, passport_id):
        '''
        根据账户id查询用户订单列表
        '''
        order_basic_list = OrderBasic.objects.get_order_list_by_passport(passport_id=passport_id)
        for order_basic in order_basic_list:
            order_detail_list = OrderDetail.objects_logic.get_order_detail_list_by_order_id(order_id=order_basic.order_id)
            order_basic.detail_list = order_detail_list
        return order_basic_list

class OrderBasicManager(BaseModelManager):
    '''
    订单基本模型管理类
    '''
    def add_one_order_basic_info(self, order_id, passport_id, addr_id,
                                 total_count, total_price, transit_price,
                                 pay_method):
        '''
        生成一个订单基本信息
        '''
        order_basic = self.create_one_object(order_id=order_id, passport_id=passport_id,
                               addr_id=addr_id, total_count=total_count,
                               total_price=total_price, transit_price=transit_price,
                               pay_method=pay_method)
        return order_basic

    def get_order_list_by_passport(self, passport_id):
        '''
        根据账户id查找用户的订单列表
        '''
        order_basic_list = self.get_object_list(filters={'passport_id':passport_id})

        return order_basic_list


class OrderBasic(BaseModel):
    '''
    订单基本类
    '''
    # 20170808101130+用户的id
    order_id = models.CharField(max_length=64, primary_key=True, help_text='订单id')
    passport = models.ForeignKey('df_user.Passport', help_text='用户')
    addr = models.ForeignKey('df_user.Address', help_text='收件地址')
    total_count = models.IntegerField(default=1, help_text='商品总数')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='商品总额')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='订单运费')
    # 1.货到付款 2.微信支付 3.支付宝支付 4.银行卡支付
    pay_method = models.IntegerField(default=1, help_text='支付方式')
    # 1.待支付 2.待发货　3.待收货 4.待评价 5.已完成
    order_status = models.IntegerField(default=1, help_text='订单状态')

    objects = OrderBasicManager()
    objects_logic = OrderBasicLogicManager()

    class Meta:
        db_table = 's_order_basic'


class OrderDetailLogicManager(BaseModelManager):
    '''
    订单详情模型逻辑管理类
    '''
    def get_order_detail_list_by_order_id(self, order_id):
        '''
        根据订单id查询订单的详情信息
        '''
        order_detail_list = OrderDetail.objects.get_order_detail_list_by_order_id(order_id=order_id)
        for order_detail in order_detail_list:
            # 根据订单中商品的id查找商品的图片
            img = Image.objects.get_image_by_goods_id(goods_id=order_detail.goods.id)
            order_detail.goods.img_url = img.img_url
        return order_detail_list


class OrderDetailManager(BaseModelManager):
    '''
    订单详情模型管理类
    '''
    def add_one_order_detail_info(self, order_id, goods_id, goods_count, goods_price):
        '''
        生成一条订单详细记录
        '''
        order_detail = self.create_one_object(order_id=order_id, goods_id=goods_id,
                               goods_count=goods_count, goods_price=goods_price)
        return  order_detail

    def get_order_detail_list_by_order_id(self, order_id):
        '''
        根据订单id查询订单的详情信息
        '''
        order_detail_list = self.get_object_list(filters={'order_id':order_id})
        return order_detail_list


class OrderDetail(BaseModel):
    '''
    订单详情类
    '''
    order = models.ForeignKey('OrderBasic', help_text='基本订单')
    goods = models.ForeignKey('df_goods.Goods', help_text='商品')
    goods_count = models.IntegerField(default=1, help_text='商品数目')
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='商品价格')

    objects = OrderDetailManager()
    objects_logic = OrderDetailLogicManager()

    class Meta:
        db_table = 's_order_detail'