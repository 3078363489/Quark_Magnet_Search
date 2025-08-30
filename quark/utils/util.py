# -*- coding: utf-8 -*-
import re
import time
import math


def get_id_from_url(url) -> str:
    """
    通过夸克的分享链接获取到pwd_id
    :param url: 夸克网盘的分享链接
    :return: 夸克网盘的pwd_id
    """
    pattern = r"/s/(\w+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return ""


def generate_timestamp(length=13):
    """
    获取时间戳
    :param length: 需要返回时间戳的长度，默认为13位
    :return: 时间戳
    """
    time.ctime()
    timestamps = str(time.time() * 1000)
    return int(timestamps[0:length])


def have_next_page(size,total,current):
    """
    判断是否存在下一页
    :param size: 单页数据数量
    :param total: 总数据数量
    :param current: 当前页码
    :return: 若有分页，返回True，否则返回False
    """
    return current < math.ceil(total / size)
