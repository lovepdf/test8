# coding=utf-8
from django.template import Library

# 创建一个Library对象--过滤器
register = Library()

@register.filter
def show_status(num):
    '''
    返回订单状态
    '''
    order_status_dict1 = {1:'待支付', 2:'待发货', 3:'代收货', 4:'待评价', 5:'已完成'}
    return order_status_dict1[num]