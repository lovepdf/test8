# coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render
from df_goods.models import Goods, BrowseHistory, Image
from df_goods.enums import *
from django.core.paginator import Paginator # 导入分页类
from django.views.decorators.http import require_GET


# Create your views here.

def home_list_page(request):
    '''
    显示商品首页内容
    '''
    # 查询某类商品最新三个
    fruits_new = Goods.objects_logic.get_goods_list_by_type(goods_type_id=FRUITS, limit=3, sort='new')
    fruits = Goods.objects_logic.get_goods_list_by_type(goods_type_id=FRUITS, limit=4)
    seafood_new = Goods.objects_logic.get_goods_list_by_type(goods_type_id=SEAFOOD, limit=3, sort='new')
    seafood = Goods.objects_logic.get_goods_list_by_type(goods_type_id=SEAFOOD, limit=4)
    meat_new = Goods.objects_logic.get_goods_list_by_type(goods_type_id=MEAT, limit=3, sort='new')
    meat = Goods.objects_logic.get_goods_list_by_type(goods_type_id=MEAT, limit=4)
    eggs_new = Goods.objects_logic.get_goods_list_by_type(goods_type_id=EGGS, limit=3, sort='new')
    eggs = Goods.objects_logic.get_goods_list_by_type(goods_type_id=EGGS, limit=4)
    vegetables_new = Goods.objects_logic.get_goods_list_by_type(goods_type_id=VEGETABLES, limit=3, sort='new')
    vegetables = Goods.objects_logic.get_goods_list_by_type(goods_type_id=VEGETABLES, limit=4)
    frozen_new = Goods.objects_logic.get_goods_list_by_type(goods_type_id=FROZEN, limit=3, sort='new')
    frozen = Goods.objects_logic.get_goods_list_by_type(goods_type_id=FROZEN, limit=4)

    # 组织模板上下文
    context = {'fruits_new': fruits_new, 'fruits': fruits,
               'seafood_new': seafood_new, 'seafood': seafood,
               'meat_new': meat_new, 'meat': meat,
               'eggs_new': eggs_new, 'eggs': eggs,
               'vegetables_new': vegetables_new, 'vegetables': vegetables,
               'frozen_new': frozen_new, 'frozen': frozen}
    return render(request, 'index.html', context=context)

def goods_detail(request, gid):
    '''
    根据商品Id 去查询商品信息
    '''
    # 1.根据商品id去查询商品信息
    goods = Goods.objects_logic.get_goods_by_id(goods_id=gid)
    # 2. 查询这个这种的最新两个商品
    goods_new_li = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods.goods_type_id,limit=2, sort='new')
    # 3. 记录用户浏览商品信息
    if request.session.has_key('passport_id'):
        # 用户登录之后才会记住密码
        passport_id = request.session.get('passport_id')
        BrowseHistory.objects.add_one_browse_history(passport_id=passport_id, goods_id=gid)
    # 4. 传递给detail.html
    return render(request, 'detail.html',{'goods':goods, 'goods_new_li':goods_new_li})


@require_GET
def goods_list(request, type_id, pindex):
    '''
    商品列表列 type: 商品种类, pindex:页码
    '''
    # 接受排序参数
    sort = request.GET.get('sort','default')
    # 根据商品种类查询商品信息
    goods_list = Goods.objects_logic.get_goods_list_by_type(goods_type_id=type_id, sort=sort)
    new_goods_list = Goods.objects_logic.get_goods_list_by_type(goods_type_id=type_id, sort='new',limit=2)
    paginator = Paginator(goods_list, 1)  # 对查询结果分页
    # 取第pindex页的数据
    pindex = int(pindex)
    goods_list = paginator.page(pindex)
    # 获取总页数
    num_pages = paginator.num_pages
    # 如果页码大于总页数,显示第一页
    if pindex > num_pages:
        pindex=1
    # 获取当前页码
    current_num = goods_list.number
    # 控制页码列表
    if num_pages<=5:
        # 显示所有页码
        pages = range(1,num_pages+1)
    elif current_num<=3:
        # 如果当前页是前三页，页码显示1-5
        pages = range(1,6)
    elif num_pages - current_num <= 2:
        # 如果当前页是后三页，页面显示后5页
        pages = range(num_pages-4,num_pages+1)
    else:
        # 显示当前页的前两页和后两页
        pages = range(current_num-2,current_num+3)
    return render(request, 'list.html', {'goods_list':goods_list, 'type_id':type_id,'sort':sort, 'pages':pages,'new_goods_list':new_goods_list})


def get_img_list(request):
    '''
    获取搜索结果页面上商品的图片列表
    '''
    # 1. 接受页面上商品的id列表
    goods_id_list = request.GET.get('goods_id_list')
    goods_id_list = goods_id_list.split(',')
    print goods_id_list
    img_list = Image.objects.get_img_list_by_goods_id_list(goods_id_list=goods_id_list)
    img_dict = {}
    for img in img_list:
        img_dict[img.goods.id] = img.img_url.name
    return JsonResponse({'img_dict':img_dict})
