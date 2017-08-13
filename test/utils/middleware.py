# coding=utf-8

class UserLoginStatusMiddleware(object):
    '''
    记录用户登录状态
    '''
    def process_request(self, request):
        '''
        url 匹配之前调用这个中间件
        '''
        # 默认用户未登录
        request.islogin = False
        # 判断用户是否登录
        if request.session.has_key('islogin'):
            # 用户已登录
            # 给request对象加一个属性，标记用户是否登录
            request.islogin = True
            # 记住用户名
            request.username = request.session['username']


class UrlPathRecordMiddleware(object):
    '''
    记录用户访问的url地址
    '''
    exclude_path = ['/user/login/', '/user/login_check/', '/user/logout/', '/user/register/', '/user/check_user_name_exist/']
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        '''
        url匹配之后视图函数调用之前会调用
        '''
        # 获取用户访问的url request.path
        urlpath = request.path
        if urlpath not in UrlPathRecordMiddleware.exclude_path:
            # 记录url地址
            request.session['url_pre_login'] = request.get_full_path()