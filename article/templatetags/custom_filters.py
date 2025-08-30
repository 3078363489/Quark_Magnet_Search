# 在your_app/templatetags/custom_filters.py中
from django import template
from django.utils.text import Truncator
import re

register = template.Library()

@register.filter
def remove_all_whitespace(value):
    """移除所有空白字符"""
    return re.sub(r'\s+', '', value)

@register.filter
def truncate_chinese_chars(value, arg):
    """专门处理中文字符的截断"""
    try:
        length = int(arg)
        if len(value) <= length:
            return value
        # 截断并添加省略号
        return value[:length-3] + '...' if length > 3 else value[:length]
    except (ValueError, TypeError):
        return value