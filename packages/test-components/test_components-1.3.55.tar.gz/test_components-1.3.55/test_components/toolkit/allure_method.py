#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/8/13
# @Author  : zxp
import allure, json
from .case_method import CaseMethod


class AllureMethod(CaseMethod):
    """
    allure 相关方法封装
    """

    @classmethod
    def save_data(cls, url, request_data, response_data, name=None, headers_data=None, response_head=None):
        if name is not None:
            with allure.step("测试步骤：%s" % name):
                pass
        if headers_data is not None:
            with allure.step("请求头参数：%s" % json.dumps(headers_data, ensure_ascii=False)):
                pass
        if isinstance(request_data, dict):
            request_data = json.dumps(request_data, ensure_ascii=False)
        with allure.step("请求地址：%s，请求参数：%s" % (url, request_data)):
            pass
        if response_head is not None:
            with allure.step("请求头返回值：%s" % json.dumps(response_head, ensure_ascii=False)):
                pass
        if isinstance(response_data, dict):
            response_data = json.dumps(response_data, ensure_ascii=False)
        with allure.step("返回值：%s" % response_data):
            pass

    @classmethod
    def save_db_data_to_report(cls, host_addr, db_name, sql_data, result_data, name=None):
        if name is None:
            name = "查询"
        with allure.step("数据库操作：%s" % name):
            pass
        with allure.step("数据库地址：%s，数据库：%s" % (host_addr, db_name)):
            pass
        with allure.step("语句：%s" % sql_data):
            pass
        with allure.step("结果：%s" % result_data):
            pass

    @classmethod
    def save_redis_data_to_report(cls, redis_data, result_data, name=None):
        if name is None:
            name = "查询"
        with allure.step("redis操作：%s" % name):
            pass
        with allure.step("操作语句：%s" % redis_data):
            pass
        with allure.step("结果：%s" % result_data):
            pass

    @classmethod
    def save_mock_data_to_report(cls, name, path=None, data=None, response_data=None):
        with allure.step(name):
            pass
        with allure.step("mock地址：%s" % path):
            pass
        with allure.step("操作数据：%s" % data):
            pass
        with allure.step("结果：%s" % response_data):
            pass

    @classmethod
    def save_http_data(cls, url, request_data, response_data, name=None, headers=None,
                       response_head=None):
        if name:
            with allure.step("测试步骤：%s" % name):
                pass
        if headers:
            with allure.step("请求头参数：%s" % json.dumps(headers, ensure_ascii=False)):
                pass
        with allure.step("请求地址：%s，请求参数：%s" % (url, json.dumps(request_data, ensure_ascii=False))):
            pass
        if response_head:
            with allure.step("请求头返回值：%s" % json.dumps(response_head, ensure_ascii=False)):
                pass
        with allure.step("返回值：%s" % json.dumps(response_data, ensure_ascii=False)):
            pass

    @classmethod
    def allure_get(cls, url, case_name, params=None, timeout=5, **kwargs):
        resp = cls.get(url, params, timeout, **kwargs)
        cls.save_http_data(url, params, resp.text, case_name, response_head=resp.headers, **kwargs)
        return resp

    @classmethod
    def allure_post(cls, url, request_data, case_name, data=None, timeout=5, **kwargs):
        resp = cls.post(url, request_data, data, timeout, **kwargs)
        cls.save_http_data(url, request_data, resp.text, case_name, response_head=resp.headers, **kwargs)
        return resp
