# coding=utf-8
from django.conf.urls import url
from df_user import views
urlpatterns = [
    url(r'^register/$', views.register), # 展示用户注册页面
    # url(r'^register_handle/$', views.register_handle),  # 注册用户信息
    url(r'^check_username_exist/$', views.check_username_exist),
    url(r'^login/$',views.login),
    url(r'^login_check/$',views.login_check),
    url(r'^address/$', views.address),  # 显示用户中心地址页面
    url(r'^logout/$',views.logout),  # 退出登录
    url(r'^$', views.user),  # 显示用户个人信息
    url(r'^order/(\d+)/$', views.order),  # 显示用户个人订单页面
]