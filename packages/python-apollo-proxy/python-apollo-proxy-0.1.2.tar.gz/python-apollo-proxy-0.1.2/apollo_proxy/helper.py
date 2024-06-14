# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-apollo
# FileName:     helper.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/04/19
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import os
import ast
import sys
import socket
import hashlib
import typing as t
from json import decoder

version = sys.version_info.major

if version == 2:
    from apollo_proxy.python_2x import *

if version == 3:
    from apollo_proxy.python_3x import *

# 定义常量
CONFIGURATIONS = "configurations"
NOTIFICATION_ID = "notificationId"
NAMESPACE_NAME = "namespaceName"


# 对时间戳，uri，秘钥进行加签
def signature(timestamp, uri, secret):
    import hmac
    import base64
    string_to_sign = '' + timestamp + '\n' + uri
    hmac_code = hmac.new(secret.encode(), string_to_sign.encode(), hashlib.sha1).digest()
    return base64.b64encode(hmac_code).decode()


def url_encode_wrapper(params):
    return url_encode(params)


def no_key_cache_key(namespace, key):
    return "{}{}{}".format(namespace, len(namespace), key)


# 返回是否获取到的值，不存在则返回None
def get_value_from_dict(namespace_cache, key):
    if namespace_cache:
        kv_data = namespace_cache.get(CONFIGURATIONS)
        if kv_data is None:
            return None
        if key in kv_data:
            return kv_data[key]
    return None


def init_ip() -> str:
    s = None
    ip = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 53))
        ip = s.getsockname()[0]
    finally:
        if isinstance(s, socket.socket):
            s.close()
        return ip


def is_json(args: str) -> bool:
    try:
        value = ast.literal_eval(args)
        if isinstance(value, list) or isinstance(value, dict) or \
                isinstance(value, bytes) or isinstance(value, bytearray):
            return True
        else:
            return False
    except (decoder.JSONDecodeError, TypeError, Exception):
        return False


def get_project_path():
    # 获取当前执行文件的绝对路径（兼容 Python 2 和 Python 3）
    exec_file_path = os.path.abspath(sys.argv[0])
    exec_file_path_slice = exec_file_path.split(os.path.sep)
    return os.path.sep.join(exec_file_path_slice[:-1])


def join_path(path_slice: list) -> t.LiteralString | str | bytes:
    return os.path.join(*path_slice)
