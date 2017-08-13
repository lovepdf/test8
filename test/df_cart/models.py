# coding=utf-8
from django.db.models import Sum
from django.db import models
from db.base_model import BaseModel
from db.base_manager import BaseModelManager
from df_goods.models import Image

# Create your models here.


class CartLogicManger(BaseModelManager):
    '''
    购物车模型逻辑管理类
    '''
    def get_cart_list_by_passport(self, passport_id):
        '''
        查询用户的购物车信息
        '''
        cart_list = Cart.objects.get_cart_list_by_passport(passport_id=passport_id)
        for cart_info in cart_list:
            # 查询商品对应的图片
            img = Image.objects.get_image_by_goods_id(goods_id=cart_info.goods.id)
            # 给商品增加一个img_url属性, 记录商品的图片路径
            cart_info.goods.img_url = img.img_url
        return cart_list

    def get_cart_list_by_id_list(self, cart_id_list):
        '''
        查找id在cart_id_list列表中的购物车信息
        '''
        cart_list = Cart.objects.get_cart_list_by_id_list(cart_id_list=cart_id_list)
        for cart_info in cart_list:
            img = Image.objects.get_image_by_goods_id(goods_id=cart_info.goods.id)
            cart_info.goods.img_url = img.img_url
        return cart_list

class CartManger(BaseModelManager):
    '''
    购物车模型管理类
    '''
    def get_one_cart_info(self, passport_id, goods_id):
        '''
        根据passport_id和goods_id 查询购物车中的信息
        '''
        cart_info = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return cart_info
    def add_one_cart_info(self, passport_id, goods_id, goods_count):
        '''
        向购物车中添加一条商品信息
        '''
        # 1 查询此用户的购物车中是否有此信息
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        # 如果有则更新
        if cart_info:
            cart_info.goods_count = cart_info.goods_count + goods_count
            cart_info.save()
        else:
            # 如果没有该商品则添加
            cart_info = self.create_one_object(passport_id=passport_id, goods_id= goods_id, goods_count=goods_count)
        return cart_info

    def get_cart_count_by_passport(self, passport_id):
        '''
        查询用户购物车中商品的数量
        '''
        goods_count_dict = self.get_object_list(filters={'passport_id':passport_id}).aggregate(Sum('goods_count'))
        # {'goods_count__sum':值}
        return goods_count_dict['goods_count__sum']

    def get_cart_list_by_passport(self, passport_id):
        '''
        查询用户购物车信息
        '''
        cart_list = self.get_object_list(filters={'passport_id':passport_id})
        return cart_list

    def get_cart_list_by_id_list(self, cart_id_list):
        '''
        查找id在cart_id_list列表中的购物车信息
        '''
        cart_list = self.get_object_list(filters={'id__in':cart_id_list})
        return cart_list

    def get_goods_count_amount_by_id_list(self, cart_id_list):
        '''
        查询id在cart_id_list列表中的购物车信息,计算出商品的数目和总价格
        '''
        cart_list = self.get_object_list(filters={'id__in':cart_id_list})
        total_count,total_price = (0,0)
        for cart_info in cart_list:
            total_count = total_count + cart_info.goods_count
            total_price = total_price + cart_info.goods_count*cart_info.goods.goods_price
        return total_price,total_count


    def update_cart_info_by_passport(self, passport_id, goods_id, goods_count):
        '''
        更新某用户购物车中某商品的信息
        '''
        # 获取此用户购物车中的这个商品信息
        cart_info = self.get_one_cart_info(passport_id=passport_id,goods_id=goods_id)
        # 判断goods_count是否大于商品的库存
        if goods_count > cart_info.goods.goods_stock:
            return False
        else:
            cart_info.goods_count =goods_count
            cart_info.save()
            return True

    def del_cart_info_by_passport(self, passport_id, goods_id):
        try:
            cart_info = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
            cart_info.delete()
            return True
        except:
            return False

class Cart(BaseModel):
    '''
    购物车类
    '''
    passport = models.ForeignKey('df_user.Passport', help_text='账户')
    goods = models.ForeignKey('df_goods.Goods', help_text='商品')
    goods_count = models.IntegerField(default=1, help_text='商品数量')

    objects = CartManger()
    objects_logic = CartLogicManger()

    class Meta:
        db_table = 's_cart'