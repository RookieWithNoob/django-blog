from django import template
from django.utils import timezone
import math

register = template.Library()

# @register.filter(name='transfer')
# def transfer(value, arg):
#     """将输出强制转换为字符串 arg """
#     return arg
#
# @register.filter()
# def lower(value):
#     """将字符串转换为小写字符"""
#     return value.lower()

# filter可以通过装饰器进行注册。若注册装饰器中携带了name参数，则其值为此filter的名称；若未携带，则函数名就是filter的名称。
# filter必须是有一到两个参数的Python函数。第一个参数是上下文本身，第二个参数则由filter提供。举个栗子，
# 在过滤器 {{ var|foo:"bar" }} 中，变量 var 为第一个参数，变量 bar 则作为第二个参数。
# 任意模板文件中
# {% load my_filters_and_tags %}
# {{ 'ABC'|transfer:'cool' }}  # 输出：'cool'
# {{ 'ABC'|lower }}  # 输出： 'abc'

# 获取相对时间
@register.filter(name='timesince_zh')
def time_since_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        return '刚刚'

    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
        return str(math.floor(diff.seconds / 60)) + "分钟前"

    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        return str(math.floor(diff.seconds / 3600)) + "小时前"

    if diff.days >= 1 and diff.days < 30:
        return str(diff.days) + "天前"

    if diff.days >= 30 and diff.days < 365:
        return str(math.floor(diff.days / 30)) + "个月前"

    if diff.days >= 365:
        return str(math.floor(diff.days / 365)) + "年前"