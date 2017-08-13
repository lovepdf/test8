# coding=utf-8
from django.conf.urls import url
from df_order import views

urlpatterns = [
   url(r'^$', views.order_show),  # 显示用户提交订单页面
   url(r'^commit/$', views.order_commit),  # 生成定单信息
]