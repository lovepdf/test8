# coding=utf-8
from datetime import datetime
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from django.http import JsonResponse
from django.shortcuts import render

from df_goods.models import Goods
from utils.deacrators import login_required
from df_cart.models import Cart
from django.db import transaction   # 事物
from df_user.models import Address
from df_order.models import OrderBasic, OrderDetail


# Create your views here.

@require_POST
@login_required
def order_show(request):
    '''
    显示用户提交订单页面
    '''
    # 接受用户数据
    cart_id_list = request.POST.getlist('cart_checked_id')
    # print cart_id_list
    # 根据cart_id_list 去查询购物车中对应的信息
    cart_list = Cart.objects_logic.get_cart_list_by_id_list(cart_id_list=cart_id_list)
    # 查找用户的默认地址
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id=passport_id)
    cart_id_list = ','.join(cart_id_list)
    return render(request, 'place_order.html', {'cart_id_list':cart_id_list,'cart_list':cart_list, 'addr':addr,'transit_price':10})

@require_POST
@login_required
@transaction.atomic
def order_commit(request):
    '''
    生成订单
    '''
    # 1. 接受用户提交的信息
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_method')
    cart_id_list = request.POST.get('cart_id_list')
    cart_id_list = cart_id_list.split(',')
    # 组织订单信息
    passport_id = request.session.get('passport_id')
    order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(passport_id)
    # 获取订单中商品的总数和总价格
    total_price,total_count = Cart.objects.get_goods_count_amount_by_id_list(cart_id_list=cart_id_list)
    transit_price = 10.0

    # 设置事务保存点
    save_id = transaction.savepoint()
    try:
        # 创建订单基本信息
        OrderBasic.objects.add_one_order_basic_info(order_id=order_id,passport_id=passport_id,addr_id=addr_id,total_count=total_count,total_price=total_price,transit_price=transit_price,pay_method=pay_method)

        # 创建订单详细信息
        cart_list = Cart.objects.get_cart_list_by_id_list(cart_id_list=cart_id_list)
        for cart_info in cart_list:
            # 判断商品库存是否充足
            if cart_info.goods_count <= cart_info.goods.goods_stock:
                # 库存充足，生成订单详细信息
                # print cart_info.goods_count,cart_info.goods.goods_stock
                OrderDetail.objects.add_one_order_detail_info(order_id=order_id,goods_id=cart_info.goods.id,goods_count=cart_info.goods_count,goods_price=cart_info.goods.goods_price)
                # print("OrderDetail")
                # 减少商品库存
                goods_stock = cart_info.goods.goods_stock - cart_info.goods_count
                # print(goods_stock)
                goods_sales = cart_info.goods_count
                # print(goods_sales)
                Goods.objects.update_goods_info(goods_id=cart_info.goods.id,goods_stock=goods_stock,goods_sales=goods_sales)
                # print("Goods.objects.update_goods_info")
                # 删除购物车中的信息
                cart_info.delete()
                # print("cart_info.delete")
            else:
                # 库存不足
                transaction.savepoint_rollback(save_id)
                return JsonResponse({'res':0})
    except Exception as e:
        # 创建订单失败
        transaction.savepoint_rollback(save_id)
        return JsonResponse({'res':2})
    # 创建订单成功，提交事物
    transaction.savepoint_commit(save_id)
    return JsonResponse({'res':1})
