#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/8/03
# @Author  : zxp
import time
import os
import operator
import shutil
from .create_parameters import GetTestParams
from .allure_method import AllureMethod

"""
*****************注意事项***********************
做为接口测试公共包,在修改已经实现方法时,要慎重,万不得以不建议
进行修改,修改时应该考虑旧方法的兼容问题, 不然会导致旧方法的用
例产生报错信息,修改公共包前应与张晓平进行确认!
2020/08/03 挖的坑 o(╥﹏╥)o 
"""


class SmallTools(GetTestParams, AllureMethod):
    """
    常规方法,添加时应注意该方法是否已经存在
    """

    @classmethod
    def get_date(cls):
        return time.strftime("%Y-%m-%d_%H:%M:%S")

    @classmethod
    def compare_dict_result(cls, original, reference, ignore=None, retain=None, result=True, assert_key_list=None,
                            need_sort=True, check_contain=False, circular_list=False, assert_full=False):
        """
        字典比对（默认相同层级）
        :param assert_key_list: 该参数为列表,对比的key
        :param retain: 该参数为列表,只对比某些字段
        :param original:原始数据
        :param reference:预期数据
        :param ignore: 该参数为列表,忽略某些字段进行比较
        :param result: 是否在方法内断言
        :param need_sort: 是否需要排序
        :param check_contain: （存在bug，请勿使用！！）不同层级（判断original与reference之间，内容多的是否包含内容少的）
        :param circular_list: 列表中元素为dict时，是否循环列表元素进行比对：
                                True：循环列表元素（以期望结果为准对比每个dict）
                                False：不循环列表元素（直接列表全量元素判断）
        :param assert_full: 是否做全量数据比对（是否允许实际结果多返回不在预期结果中的字段）
        """
        if assert_key_list is None:
            if assert_full:
                assert_key_list = cls.get_dict_pk_key(original, [])
            else:
                assert_key_list = cls.get_dict_pk_key(reference, [])
        if retain is not None:
            assert_key_list = retain
        if check_contain:
            # 存在bug，请勿使用！！！
            # 存在bug，请勿使用！！！
            # 存在bug，请勿使用！！！
            real_origin, real_reference, assert_key_list = cls.check_origin_and_reference(original, reference)
            if ignore is not None:
                for i in ignore:
                    if i in assert_key_list:
                        assert_key_list.remove(i)
            return cls.compare_contain_dict(real_origin, real_reference, assert_key_list, result, need_sort, circular_list, assert_full)
        if ignore is not None:
            for i in ignore:
                if i in assert_key_list:
                    assert_key_list.remove(i)
        return cls.compare_dict(original, reference, assert_key_list, result, need_sort, circular_list, assert_full)

    @classmethod
    def get_dict_pk_key(cls, dict_data, key_list):
        """
        提取字典key
        :param dict_data:被提取字典
        :param key_list: 键值
        :return:
        """
        for key in dict_data.keys():
            key_list.append(key)
        return key_list

    @classmethod
    def get_dict_key(cls, dict_data, key_list):
        """
        提取字典嵌套key
        :param dict_data:被提取字典
        :param key_list: 键值
        :return:
        """
        for key in dict_data.keys():
            key_list.append(key)
            if isinstance(cls.get_dict_value(dict_data, key), dict):
                cls.get_dict_key(cls.get_dict_value(dict_data, key), key_list)
            if isinstance(cls.get_dict_value(dict_data, key), list):
                for i in cls.get_dict_value(dict_data, key):
                    if isinstance(i, dict):
                        cls.get_dict_key(i, key_list)

        return key_list

    @classmethod
    def get_dict_value(cls, dict_data, key_id):
        """
        提取字典值
        :param dict_data:被提取字典
        :param key_id: 键值
        :return:
        """
        for key in dict_data.keys():
            if key == key_id:
                return dict_data[key]
            if isinstance(dict_data[key], dict):
                value = cls.get_dict_value(dict_data[key], key_id)
                # 之前挖的坑,不判断 is not None 会导致 直接 return 会导致字典嵌套后的value 拿不到,考虑到兼容问题故只能以这种方式解决
                if value is not None:
                    return value
            if isinstance(dict_data[key], list):
                for i in dict_data[key]:
                    if isinstance(i, dict):
                        value = cls.get_dict_value(i, key_id)
                        if value is not None:
                            return value

    @classmethod
    def compare_dict(cls, original, reference, key_list, result, need_sort, circular_list, assert_full):
        """
        字典比较
        :param original:
        :param reference:
        :param key_list:
        :param result: 是否在方法列断言
        :param need_sort: 是否对列表进行排序后再比对
        :param circular_list: 列表中元素为dict时，是否循环列表元素进行比对：
                                True：循环列表元素（以期望结果为准对比每个dict）
                                False：不循环列表元素（直接列表全量元素判断）
        :param assert_full: 是否做全量数据比对（是否允许实际结果多返回不在预期结果中的字段）
        :return:
        """
        original_keys = []
        reference_keys = []
        original_keys = cls.get_dict_pk_key(original, original_keys)
        reference_keys = cls.get_dict_pk_key(reference, reference_keys)
        if assert_full:
            if result:
                assert original_keys == reference_keys, "全量断言失败，存在字段缺失情况，期望字段列表：%s，实际字段列表：%s，期望结果：%s，实际结果：%s" % (
                    reference_keys, original_keys, reference, original)
            else:
                return False
        if len(key_list) != 0:
            for key in key_list:
                # 判断key是否存在于original_keys和reference_keys
                if key in original_keys and key in reference_keys:
                    if isinstance(cls.get_dict_value(original, key), dict):
                        # 如果是字典类型
                        cls.compare_dict(original[key], reference[key], cls.get_dict_pk_key(reference[key], []),
                                         result, need_sort, circular_list, assert_full)
                    if isinstance(cls.get_dict_value(original, key), list):
                        if need_sort:
                            # 如果是列表类型
                            if len(original[key]) > 0 and len(reference[key]) > 0:
                                if assert_full:
                                    if result:
                                        assert len(original[key]) == len(reference[
                                                                             key]), "全量断言失败，列表长度不符，期望列表长度：%s，实际列表长度：%s，期望结果：%s，实际结果：%s" % (
                                            len(reference[key]), len(original[key]), reference, original)
                                    else:
                                        return False
                                if len(original[key]) < len(reference[key]):
                                    if result:
                                        assert False, "列表长度不符，期望列表长度：%s，实际列表长度：%s，期望结果：%s，实际结果：%s" % (
                                            len(reference[key]), len(original[key]), reference, original)
                                    else:
                                        return False
                                if isinstance(original[key][0], dict):
                                    # 如果列表里是字典，则按照第一个key排序
                                    sorted_keys = cls.get_dict_pk_key(original[key][0], [])
                                    str_sorted_key = ""
                                    for sorted_key in sorted_keys:
                                        # 取非dict且非list的key
                                        if not isinstance(original[key][0][sorted_key], dict) and not isinstance(
                                                original[key][0][sorted_key], list):
                                            str_sorted_key = sorted_key
                                            break
                                    if str_sorted_key == "":
                                        for index in range(len(reference[key])):
                                            cls.compare_dict(original[key][index], reference[key][index],
                                                             cls.get_dict_pk_key(reference[key][index], []),
                                                             result, need_sort, circular_list, assert_full)
                                    else:
                                        try:
                                            sorted_origin = sorted(original[key],
                                                                   key=operator.itemgetter(str_sorted_key))
                                            sorted_reference = sorted(reference[key],
                                                                      key=operator.itemgetter(str_sorted_key))
                                        except:
                                            sorted_origin = original[key]
                                            sorted_reference = reference[key]
                                        # 继续递归列表中的元素，以期望结果的key进行对比
                                        if circular_list:
                                            for index in range(len(sorted_origin)):
                                                circular_list_result = cls.compare_dict(sorted_origin[index],
                                                                                        sorted_reference[index],
                                                                                        cls.get_dict_pk_key(
                                                                                            sorted_reference[index],
                                                                                            []),
                                                                                        result, need_sort,
                                                                                        circular_list, assert_full)
                                                if circular_list_result is False:
                                                    return False
                                        else:
                                            if result:
                                                for son_index in sorted_reference:
                                                    # 断言列表里origin存在于reference中
                                                    assert son_index in sorted_origin, "%s 预期结果：%s 不存在于实际结果：%s 中" % (
                                                        key, son_index, sorted_origin)
                                            else:
                                                return sorted_origin == sorted_reference
                                else:
                                    # 获取两列表差集
                                    dif_set = list(set(original[key]).difference(set(reference[key])))
                                    if result:
                                        assert dif_set == [] and len(original[key]) == len(reference[key]), \
                                            "key：%s 预期：%s，实际：%s，完整预期结果：%s，完整实际结果：%s" % (
                                                key, reference[key], original[key], reference, original)
                                    else:
                                        return dif_set == [] and len(original[key]) == len(reference[key])
                            else:
                                assert len(original[key]) == 0 and len(
                                    reference[key]) == 0, "key：%s 预期：%s，实际：%s" % (
                                    key, reference[key], original[key])
                        else:
                            if result:
                                assert original[key] == reference[
                                    key], "key：%s 预期：%s，实际：%s，完整预期结果：%s，完整实际结果：%s" % (
                                    key, reference[key], original[key], reference, original)
                    if not isinstance(original[key], dict) and not isinstance(original[key], list):
                        # 如果非字典和列表，则直接比较是否相等
                        if result:
                            assert cls.get_dict_value(original, key) == cls.get_dict_value(reference, key), \
                                "key：%s 预期：%s，实际：%s，完整预期结果：%s，完整实际结果：%s" % (
                                    key, cls.get_dict_value(reference, key), cls.get_dict_value(original, key),
                                    reference, original)
                        else:
                            if cls.get_dict_value(original, key) == cls.get_dict_value(reference, key):
                                pass
                            else:
                                return False
                else:
                    if result:
                        assert False, "实际结果中缺少了 %s 字段，预期结果：%s，实际结果：%s" % (key, reference, original)
                    else:
                        return False
        elif original_keys == [] or reference_keys == []:
            if result:
                assert original == reference, "预期：%s，实际：%s" % (reference, original)
            else:
                return original == reference
        else:
            raise Exception('空列表')

    @classmethod
    def check_origin_and_reference(cls, before_original, before_reference):
        """
        比较before_original和before_reference哪个范围更大
        :param before_original: 原始origin
        :param before_reference: 原始reference
        :return:
        """
        before_original_keys = cls.get_dict_key(before_original, [])
        before_reference_keys = cls.get_dict_key(before_reference, [])
        if len(before_original_keys) <= len(before_reference_keys):
            real_original = before_original
            real_reference = before_reference
        else:
            real_original = before_reference
            real_reference = before_original
        assert_key_list = cls.get_dict_pk_key(real_original, [])
        return real_original, real_reference, assert_key_list

    @classmethod
    def compare_contain_dict(cls, original, reference, key_list, result, need_sort, circular_list, assert_full):
        """
        字典比较（可以是不同层级）
        :param original:
        :param reference:
        :param key_list:
        :param result:
        :param need_sort:
        :return:
        """
        original_keys = cls.get_dict_key(original, [])
        reference_keys = cls.get_dict_key(reference, [])
        if len(key_list) != 0:
            for key in key_list:
                # 判断key是否存在于original_keys和reference_keys
                if key in original_keys and key in reference_keys:
                    origin_value = cls.get_dict_value(original, key)
                    reference_value = cls.get_dict_value(reference, key)
                    if isinstance(origin_value, dict):
                        # 如果是字典类型
                        if result:
                            cls.compare_dict(origin_value, reference_value, cls.get_dict_pk_key(origin_value, []),
                                             result, need_sort, circular_list, assert_full)
                        else:
                            return cls.compare_dict(origin_value, reference_value,
                                                    cls.get_dict_pk_key(origin_value, []), result, need_sort, circular_list, assert_full)
                    if isinstance(origin_value, list):
                        if need_sort:
                            # 如果是列表类型
                            if len(origin_value) > 0:
                                if isinstance(origin_value[0], dict):
                                    # 如果列表里是字典，则按照第一个key排序
                                    sorted_keys = cls.get_dict_pk_key(origin_value[0], [])
                                    sorted_origin = sorted(origin_value, key=operator.itemgetter(sorted_keys[0]))
                                    # bug之一就在这里↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
                                    sorted_reference = sorted(origin_value, key=operator.itemgetter(sorted_keys[0]))
                                    if result:
                                        assert sorted_origin == sorted_reference, "%s 预期：%s，实际：%s" % (
                                            key, sorted_reference, sorted_origin)
                                    else:
                                        return sorted_origin == sorted_reference
                                else:
                                    # 获取两列表差集
                                    dif_set = list(set(origin_value).difference(set(reference_value)))
                                    if result:
                                        assert dif_set == [] and len(origin_value) == len(reference_value), \
                                            "%s 预期：%s，实际：%s" % (key, reference_value, origin_value)
                                    else:
                                        return dif_set == [] and len(origin_value) == len(reference_value)
                            else:
                                if result:
                                    assert len(origin_value) == 0 and len(reference_value) == 0, "%s 预期：%s，实际：%s" % (
                                        key, reference_value, origin_value)
                                else:
                                    return len(origin_value) == 0 and len(reference_value) == 0

                        else:
                            if result:
                                assert origin_value == reference_value, "%s 预期：%s，实际：%s" % (
                                    key, reference_value, origin_value)
                    if not isinstance(origin_value, dict) and not isinstance(origin_value, list):
                        # 如果非字典和列表，则直接比较是否相等
                        if result:
                            assert origin_value == reference_value, "%s 预期：%s，实际：%s" % (
                                key, reference_value, origin_value)
                        else:
                            return origin_value == reference_value
                else:
                    raise Exception('列表存在错误key', key, "\n", key_list)
        elif original_keys == [] or reference_keys == []:
            if result:
                assert original == reference, "预期：%s，实际：%s" % (reference, original)
            else:
                return original == reference
        else:
            raise Exception('空列表')

    @classmethod
    def except_output(cls, finally_func=None):
        def except_func(func):
            """
            异常处理装饰器
            :param func:
            :return:
            """

            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(e)
                    if finally_func is not None:
                        finally_func()

            return wrapper

        return except_func

    @classmethod
    def project_directory(cls, path_file=__file__, split_path_list=None):
        """
        项目路径
        :param split_path_list: type list
        :param path_file:
        :return:
        """
        cur_path = os.path.abspath(os.path.dirname(path_file))
        if split_path_list is not None and type(split_path_list) is list:
            for i in split_path_list:
                path = cur_path.split(i)[0]
            return path
        return cur_path

    @classmethod
    def root_path(cls, path):
        """
        拼接项目路径
        :param path: os.path.dirname(__file__)
        :return:
        """
        cur_path = os.path.abspath(path)
        root_path = os.path.join(os.path.split(cur_path)[0],
                                 os.path.split(cur_path)[1]
                                 )
        return root_path

    @classmethod
    def del_all_file(cls, del_path, filter_file=None):
        """
        :param del_path: 删除文件夹or 文件
        :param filter_file: 过滤文件后缀
        :return:
        """
        for i in os.listdir(del_path):
            file_data = del_path + "/" + i
            if os.path.isfile(file_data) is True:
                if filter_file and filter_file not in file_data:
                    os.remove(file_data)
                else:
                    os.remove(file_data)
            elif os.path.isdir(file_data):
                shutil.rmtree(file_data)
