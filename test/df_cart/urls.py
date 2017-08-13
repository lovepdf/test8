# coding=utf-8
from django.conf.urls import url
from df_cart import views

urlpatterns = [
    url(r'^add/$',views.cart_add),  # 向购物车中添加信息
    url(r'^count/$', views.cart_count),  # 获取用户购物车中商品的数量
    url(r'^$', views.cart_show),  # 显示购物车
    url(r'^update/$', views.cart_update),  # 更新某个用户的购物车中某个商品的信息
    url(r'^del/$', views.cart_del),  # 删除用户购物车中的商品
]