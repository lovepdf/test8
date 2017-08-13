# coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from df_cart.models import Cart
from df_goods.models import Goods
from utils.deacrators import login_required

# Create your views here.


def cart_add(request):
    '''
    向购物车中添加商品
    '''
    # 获取商品id 和数量
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    # 获取登录账户的id
    passport_id = request.session.get('passport_id')
    # 3.像购物车中添加信息
    # 3.1,获取商品的库存，判断库存是否充足
    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    # 3.2, 如果充足，则添加购物车信息，返回json{'res':1}
    if int(goods_count)>goods.goods_stock:
        # 3.3 如果库存不足，返回json{'res':0}
        return JsonResponse({'res':0})
    else:
        Cart.objects.add_one_cart_info(passport_id=passport_id,goods_id=goods_id,goods_count=int(goods_count))
        return JsonResponse({'res':1})


@require_GET
@login_required
def cart_count(request):
    '''
    获取用户购物车中商品的数量
    '''
    # 获取用户的Id
    passport_id = request.session.get('passport_id')
    # 根据用户的id查询用户购物车中商品的数量
    goods_count = Cart.objects.get_cart_count_by_passport(passport_id=passport_id)
    if goods_count is None:
        goods_count =0
    return JsonResponse({'res':goods_count})

@login_required
def cart_show(request):
    '''
    显示购物车页面
    '''
    passport_id = request.session.get('passport_id')
    # 根据账户id查询用户购物车中的信息
    cart_list = Cart.objects_logic.get_cart_list_by_passport(passport_id=passport_id)
    # 查询用户购物车中的总数
    goods_count = Cart.objects.get_cart_count_by_passport(passport_id=passport_id)
    if goods_count is None:
        goods_count = 0
    return render(request, 'cart.html', {'cart_list':cart_list, 'goods_count':goods_count})


@require_GET
@login_required
def cart_update(request):
    '''
    更新购物车中商品的信息
    '''
    # 接受商品的信息和商品的数量
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')
    # 更新购物车中商品的信息update_cart_info_by_passport(passport_id,goods_id,goods_count)
    res = Cart.objects.update_cart_info_by_passport(passport_id=passport_id,goods_id=goods_id,goods_count=int(goods_count))
    # 根据更新结果返回json数据
    if res:
        # 更新成功
        return JsonResponse({'res':1})
    else:
        return JsonResponse({'res':0})

def cart_del(request):
    '''
    删除用户购物车中的某个商品
    '''
    goods_id = request.GET.get('goods_id')
    passport_id = request.session.get('passport_id')
    # 删除用户购物车中的某个商品
    res = Cart.objects.del_cart_info_by_passport(passport_id=passport_id, goods_id=goods_id)
    if res:
        return JsonResponse({'res':1})
    else:
        return JsonResponse({'res':0})