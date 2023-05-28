# -*- coding: utf-8 -*-
# @Author: XuTianDe
# @Date: 2023-05-22 19:40:11

# 密码处理
from django.conf import settings
import hashlib


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))  # 使用settings.SECRET_KEY自带的密文
    obj.update(data_string.encode('utf-8'))  # 将md5对象更新为给编码过的data_string
    return obj.hexdigest()
