#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/8/03
# @Author  : zxp
import os
from toolkit.tools import SmallTools


def a():
    failed = 1
    total = 0
    passed = 1
    if total == 0:
        logger_data = "执行异常,总用例数:%s" % total
    # fix:没有用例执行成功 导致 ZerDivisionError: division by zero
    else:
        logger_data = "成功:%s(%.2f%%);失败:%s(%.2f%%)" % (
            passed, (passed / total) * 100, failed, (failed / total) * 100)
    print(33)
    print(logger_data)


def aa(**kwargs):
    print(kwargs)
    save_data(**kwargs)


def save_data(name=None, headers_data=None, response_head=None):
    print(name)
    print(headers_data)
    print(response_head)

import requests

if __name__ == '__main__':
    import json
    d =-1
    print(json.dumps(d, ensure_ascii=False))
    # with requests.post(url="http://192.168.5.203:31647/task",json={"task_tag": 2222,
    #     "version": "release"})as resp:
    #     print(resp.text)
    #     print(resp.headers)
    # aa(headers=23)


# def except_output(func):
#     """
#     异常处理装饰器
#     :param func:
#     :return:
#     """
#
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             print(e)

# return wrapper
# def except_output(finally_func=None):
#     def except_func(func):
#         """
#         异常处理装饰器
#         :param func:
#         :return:
#         """
#
#         def wrapper(*args, **kwargs):
#             try:
#                 return func(*args, **kwargs)
#             except Exception as e:
#                 print(e)
#                 if finally_func is None:
#                     finally_func
#                 else:
#                     print(finally_func)
#         return wrapper
#     return except_func
#
# def b():
#     print('www')
#     with open("test.txt","w")as s:
#         s.write("ww")
#
# @except_output("test")
# def a():
#     l=[]
#     print(l[0])
#
def a(path_file=__file__):
    cur_path = os.path.abspath(os.path.dirname(path_file))
    return cur_path.split()[0].split("\\")[len(cur_path.split()[0].split("\\")) - 1]


class test():
    @classmethod
    def project_directory(cls, path_file=__file__, split_path=None):
        """
        项目路径
        :param split_path: type list
        :param path_file:
        :return:
        """
        cur_path = os.path.abspath(os.path.dirname(path_file))
        print(cur_path.split()[0].split("\\")[len(cur_path.split()[0].split("\\")) - 1])
        print(len(cur_path.split()[0].split("\\")))
        if split_path is not None and type(split_path) is list:
            for i in split_path:
                print(i)
                path = cur_path.split(i)[0]
            return path
        return cur_path


def df(root_path, *args, cpu='auto', case_path=None, limited_time=30, report_path=None,
       has_special=False, **kwargs):
    if kwargs.get("a"):
        print(1111111)
    print(case_path)


class Person(object):
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    @property
    def get_age_fun(self):
        return self.__age

    @get_age_fun.setter  # get_age_fun是上面声明的方法
    def set_age_fun(self, value):
        if not isinstance(value, int):
            raise ValueError('年龄必须是数字!')
        if value < 0 or value > 100:
            raise ValueError('年龄必须是0-100')
        self.__age = value

    def print_info(self):
        print('%s: %s' % (self.__name, self.__age))

    # import uuid,time
    # def get_uuid():
    #     return str(uuid.uuid4()).replace("-", '')
    #
    #
    # def es_info(path, request, response, msg, trace_id=get_uuid(), level="Error"):
    #     return {
    #         "trace_id": trace_id,
    #         'path': path,
    #         'request': request,
    #         'response': response,
    #         'level': level,
    #         'msg': msg,
    #         'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     }
    #
    #
    # from toolkit.kibana_method import Es
    # df = Es("test_report_server")
    # df.logger_init()
    # df.es_info(es_info("/test", {
    #     "server_id": 101,
    #     "grade": 1,
    #     "name": "zxp",
    #     "task_num": 10,
    #     "options": 3
    # }, str({
    #     "device_id": [
    #         "zxp0_la6bAd2h37"
    #     ],
    #     "info": "success"
    # }), "success"))
