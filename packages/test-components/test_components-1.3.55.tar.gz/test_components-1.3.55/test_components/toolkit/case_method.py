#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/8/13
# @Author  : zxp

import requests


class CaseMethod(object):
    """
    请求相关在此处定义
    """

    @classmethod
    def post(cls, url, request_data, data=None, timeout=5, **kwargs):
        if data is None:
            with requests.post(url, json=request_data, timeout=timeout, **kwargs) as resp:
                return resp
        else:
            with requests.post(url, data=data, timeout=timeout, **kwargs) as resp:
                return resp

    @classmethod
    def put(cls, url, data=None, timeout=5, **kwargs):
        with requests.put(url, data=data, timeout=timeout, **kwargs) as resp:
            return resp

    @classmethod
    def delete(cls, url, timeout=5, **kwargs):
        with requests.delete(url, timeout=timeout, **kwargs) as resp:
            return resp

    @classmethod
    def get(cls, url, params=None, timeout=5, **kwargs):
        with requests.get(url, params=params, timeout=timeout, **kwargs) as resp:
            return resp

    @classmethod
    def patch(cls, url, data=None, timeout=5, **kwargs):
        with requests.patch(url, data=data, timeout=timeout, **kwargs) as resp:
            return resp
