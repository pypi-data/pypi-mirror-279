# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-apollo
# FileName:     python_2x.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/04/19
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import urllib2
from urllib import urlencode
from .logger_handler import logger


def http_request(url, timeout, headers=None):
    try:
        request = urllib2.Request(url, headers=headers)
        res = urllib2.urlopen(request, timeout=timeout)
        body = res.read().decode("utf-8")
        return res.code, body
    except urllib2.HTTPError as e:
        logger.warning("http_request error,code is %d, msg is %s", e.code, e.msg)


def url_encode(params):
    return urlencode(params)
