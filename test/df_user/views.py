# coding=utf-8
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from df_user.models import Passport, Address
from df_goods.models import BrowseHistory
from df_order.models import OrderBasic
from hashlib import sha1
from django.http import JsonResponse
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from utils.deacrators import login_required  # 导入访问视图函数装饰器


# Create your views here.
@require_http_methods(['GET','POST'])
def register(request):
    '''
    展示用户注册页面
    '''
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        '''
        注册用户信息
        '''
        # 接受用户的注册信息
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')

        # 创建新用户
        Passport.objects.add_one_passport(username=username, password=password, email=email)

        # 跳转到首页
        return redirect('/')

'''
@require_POST
def register_handle(request):

    注册用户信息

    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')

    # 创建新用户
    Passport.objects.add_one_passport(username=username,password=password,email=email)

    # 跳转到首页
    return render(request, 'login.html')
'''



def check_username_exist(request):
    '''
    校验用户名是否已经注册
    '''
    # 接受用户名
    username = request.GET.get('username')
    # 根据用户名查找账户信息
    passport = Passport.objects.get_one_passport(username=username)
    if passport:

        return JsonResponse({'res':0})
    else:
        return JsonResponse({'res':1})


def login(request):
    '''
    显示用户登录页面
    '''
    username = ''
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
    return render(request, 'login.html', {'username':username})

@require_POST
def login_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    passport = Passport.objects.get_one_passport(username=username,password=password)
    if passport:
        # 用户名和密码正确
        # return JsonResponse({'res':1})
        if request.session.has_key('url_pre_login'):
            next = request.session.get('url_pre_login')
        else:
            # 默认跳转到首页
            next = '/'
        jres = JsonResponse({'res':1, 'next':next})
        # 是否需要记住用户名
        remember = request.POST.get('remember')
        if remember == 'true':
            # true 为需要记住用户名,将用户名保存在cookie中
            jres.set_cookie('username',username)
        else:
            # 用户名或密码错误
            jres.delete_cookie('username')

        # 记住用户的登录状态
        request.session['islogin'] = True
        request.session['passport_id'] = passport.id
        request.session['username'] = username
        return jres
    else:
        # 用户名或密码错误
        return JsonResponse({'res':0})

def logout(request):
    '''
    退出登录
    '''
    request.session.flush()  # 删除用户的session信息
    return redirect('/')

def user(request):
    '''
    显示用户中心地址页面
    '''
    # 获取用户的账户Id
    passport_id = request.session.get('passport_id')
    # 查找账户默认地址
    addr = Address.objects.get_default_address(passport_id=passport_id)
    # 查找用户浏览历史记录
    browse_li = BrowseHistory.objects_logic.get_browse_list_by_passport(passport_id=passport_id, limit=5)
    return render(request, 'user_center_info.html', {'addr':addr,'browse_li':browse_li,'page':'user'})


@login_required
def address(request):
    '''
     显示用户中心地址页面
    '''
    # 获取用户id
    passport_id = request.session.get('passport_id')
    if request.method == 'GET':
        # 显示用户中心地址页面
        #　１．查找用户是否存在默认地址
        addr = Address.objects.get_default_address(passport_id=passport_id)
        return render(request, 'user_center_site.html', {'request':request, 'addr':addr, 'page':'addr'})
    else:

        # 1.接受收件地址信息
        recipicent_name = request.POST.get('name')
        recipicent_addr = request.POST.get('addr')
        recipicent_phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')
        # 2.添加用户收件地址信息
        Address.objects.add_one_address(passport_id=passport_id, recipicent_name=recipicent_name, recipicent_addr=recipicent_addr,
                                        recipicent_phone=recipicent_phone, zip_code=zip_code)
        # 3.重定向'/user/address'
        return redirect('/user/address/')


def order(request, pindex):
    '''
    显示用户的订单页面
    '''
    # 获取账户的id
    passport_id = request.session.get('passport_id')
    order_basic_list = OrderBasic.objects_logic.get_order_list_by_passport(passport_id=passport_id)
    paginator = Paginator(order_basic_list, 1)  # 对查询结果分页
    # 参数pindex转化为整数
    pindex = int(pindex)
    # 获取总页数
    num_pages = paginator.num_pages
    # 如果页码出现总页数,显示第一页
    if pindex > num_pages:
        pindex=1
    # 获取第pindex页的数据
    order_basic_list = paginator.page(pindex)
    # 获取当前页码
    current_num = order_basic_list.number
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
    return render(request, 'user_center_order.html', {'order_basic_list':order_basic_list, 'page':'order', 'pages':pages})