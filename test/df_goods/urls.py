# coding=utf-8
from django.conf.urls import url
from df_goods import views
urlpatterns = [
    url(r'^$', views.home_list_page),  # 显示商品首页
    url(r'^(\d+)/$', views.goods_detail),  # 显示商品详情页面
    url(r'^list/(\d+)/(\d+)/', views.goods_list),  # 商品列表
    url(r'^get_img_list/$', views.get_img_list),  # 获取商品图片列表
]