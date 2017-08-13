# coding=utf-8
from django.db import models
from db.base_model import BaseModel
from db.base_manager import BaseModelManager
from tinymce.models import HTMLField

from df_goods.enums import *
# Create your models here.


class GoodsLogicManger(BaseModelManager):
    '''
    商品模型逻辑管理类
    '''
    def get_goods_by_id(self, goods_id):
        '''
        根据id去获取某个商品信息
        '''
        # 首先调用Goods.objectsManger的get_goods_by_id方法获取商品信息
        goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
        # 查询出商品图片
        img = Image.objects.get_image_by_goods_id(goods_id=goods_id)
        if goods:
            # 给商品加一个img_url，记录商品图片路径
            goods.img_url = img.img_url
            goods.type_title = GOODS_TYPE[goods.goods_type_id]
        return goods

    def get_goods_list_by_type(self, goods_type_id, limit=None,sort='default'):
        '''
        根据商品类型查询商品信息:包含商品图片路径
        '''
        # 首先调用GoodsManger的get_goods_list_by_type方法获取商品信息
        goods_list = Goods.objects.get_goods_list_by_type(goods_type_id=goods_type_id, limit=limit, sort=sort)
        for goods in goods_list:
            # 查询出商品的图片
            img = Image.objects.get_image_by_goods_id(goods_id=goods.id)
            # 给商品加一个属性img_url, 记录商品图片路径
            goods.img_url = img.img_url
        return goods_list



class GoodsManger(BaseModelManager):
    '''
    商品模型管理类
    '''
    def get_goods_by_id(self, goods_id):
        '''
        根据id获取某个商品信息
        '''
        goods = self.get_one_object(id=goods_id)
        return goods

    def get_goods_list_by_type(self,goods_type_id,limit=None,sort='default'):
        '''
        根据商品类型查询商品信息
        '''
        if sort == 'new':
            # 查询新品
            goods_list = self.get_object_list(filters={'goods_type_id':goods_type_id}, order_by=('-create_time',))
        elif sort == 'price':
            # 根据价格来查商品
            goods_list = self.get_object_list(filters={'goods_type_id': goods_type_id}, order_by=('goods_price',))
        elif sort == 'hot':
            # 根据人气来查商品
            goods_list = self.get_object_list(filters={'goods_type_id': goods_type_id}, order_by=('-goods_sales',))
        else:
            # 按照默认方式查询商品
            goods_list = self.get_object_list(filters={'goods_type_id': goods_type_id})
        if limit:
            goods_list = goods_list[:limit]
        return goods_list

    def update_goods_info(self, goods_id, goods_stock, goods_sales):
        '''
        更新商品信息
        '''
        # 查询出对应的商品信息并加锁
        try:
            goods = self.select_for_update().get(id=goods_id)
            # print(goods)
            goods.goods_stock = goods_stock
            # print(goods.goods_stock)
            goods.goods_sales += goods_sales
            # print(goods.goods_sales)
            goods.save()
            # print("goods.save")
            return True
        except:
            return False

class Goods(BaseModel):
    '''
    商品类
    '''
    '''
    全局变量
    goods_type_choice = (
        (FRUITS, GOODS_TYPE[FRUITS]),
        (SEAFOOD, GOODS_TYPE[SEAFOOD]),
        (MEAT, GOODS_TYPE[MEAT]),
        (EGGS, GOODS_TYPE[EGGS]),
        (VEGETABLES, GOODS_TYPE[VEGETABLES]),
        (FROZEN, GOODS_TYPE[FROZEN]),
    )
    '''
    # 获取商品种类选择项
    goods_type_choice = ((k,v)for k,v in GOODS_TYPE.items())
    goods_type_id = models.SmallIntegerField(choices=goods_type_choice, help_text='商品种类')

    goods_name = models.CharField(max_length=32, help_text='商品名称')
    goods_sub_title = models.CharField(max_length=128, help_text='商品副标题')
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='商品价格')
    goods_ex_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='商品运费')
    goods_unite = models.CharField(max_length=16, default='500g', help_text='商品单位')
    goods_info = HTMLField(help_text='商品描述')
    goods_stock = models.IntegerField(default=1, help_text='商品库存')
    # 0.商品上线　１：商品下线
    goods_status = models.SmallIntegerField(default=0, help_text='商品状态')
    goods_sales = models.IntegerField(default=0, help_text='商品销量')

    # 自定义一个商品模型管理器对象
    objects = GoodsManger()
    # 自定义一个商品模型逻辑管理器对象：如果查询的商品信息想要包含图片信息可以通过这个对象
    objects_logic = GoodsLogicManger()

    class Meta:
        db_table = 's_goods'


# =====================商品图片相关====================

class ImageManger(BaseModelManager):
    '''
    图片模型管理器类
    '''
    def get_image_by_goods_id(self, goods_id):
        '''
        根据商品id获取商品图片
        '''
        img = self.get_object_list(filters={'goods_id':goods_id})
        if img.exists():
            img = img[0]
        else:
            img.img_url = ''
        return img

    def get_img_list_by_goods_id_list(self, goods_id_list):
        '''
        根据商品的id列表查询图片列表
        '''
        img_list = self.get_object_list(filters={'goods_id__in':goods_id_list})
        # print img_list
        return img_list


class Image(BaseModel):
    '''
    商品图片类
    '''
    goods = models.ForeignKey('Goods', help_text='所属商品')
    img_url = models.ImageField(upload_to='goods', help_text='图片路径')
    is_def = models.BooleanField(default=False, help_text='是否默认')

    objects = ImageManger()

    class Meta:
        db_table = 's_goods_image'


# ============================历史浏览记录==============================
class BrowseHistoryLogicManager(BaseModelManager):
    '''
    历史浏览模型管理器类
    '''
    def get_browse_list_by_passport(self, passport_id, limit=None):
        '''
        查询某个用户的历史浏览记录: 包含图片路径
        '''
        browse_list = BrowseHistory.objects.get_browse_list_by_passport(passport_id=passport_id, limit=limit)
        for browse in browse_list:
            img = Image.objects.get_image_by_goods_id(goods_id=browse.goods.id)
            browse.goods.img_url = img.img_url
        return browse_list

class BrowseHistoryManager(BaseModelManager):
    '''
    历史浏览模型管理器类
    '''
    def get_browse_list_by_passport(self, passport_id, limit=None):
        '''
        查询某个用户的历史浏览记录
        '''
        browse_list = self.get_object_list(filters={'passport_id':passport_id},order_by=('-update_time',))
        if limit:
            browse_list = browse_list[:limit]
        return browse_list
    def is_user_browsed_goods(self, passport_id, goods_id):
        '''
        查看用户是否浏览过次商品
        '''
        browse = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return browse
    def add_one_browse_history(self, passport_id, goods_id):
        '''
        添加用户浏览的商品信息
        '''
        # 1. 判断用户是否已经浏览过次商品
        browse = self.is_user_browsed_goods(passport_id=passport_id, goods_id=goods_id)
        if browse:
            # 有此产品信息,更新时间
            browse.save()
        else:
            browse = self.create_one_object(passport_id=passport_id, goods_id=goods_id)
        return browse

class BrowseHistory(BaseModel):
    '''
    历史浏览商品类
    '''
    passport = models.ForeignKey('df_user.Passport', help_text='账户')
    goods = models.ForeignKey('Goods', help_text='商品')

    objects = BrowseHistoryManager()
    objects_logic = BrowseHistoryLogicManager()

    class Meta:
        db_table = 's_browse_history'