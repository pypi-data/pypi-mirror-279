# -*-coding:UTF-8 -*-
# @Time    : 2019-10-14 14:28:12
# @Author  : lsf

import copy, collections, string, random

from collections.abc import Iterable

import math
import uuid


class GetTestParams(object):
    """
    构造异常测试数据,调用get_all_exception_test_data()
    获取到数据列表,之后同个PYtest框架里的parametrize()方
    法进行循环
    """

    @classmethod
    def generate_random_str(cls, random_length=16):
        """
        生成一个指定长度的随机字符串，其中
        string.digits=0123456789
        string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
        """
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(random_length)]
        random_str = ''.join(str_list)
        return random_str

    @classmethod
    def generate_random_int(cls, random_length=8):
        """
        生成一个指定长度的随机数字
        """
        random_int = random.randint(math.pow(10, (random_length - 1)), math.pow(10, random_length) - 1)
        return random_int

    @classmethod
    def get_null_value_list(cls, value):
        """
        构造空数据
        """
        if isinstance(value, str):
            return ["", None]
        elif isinstance(value, int):
            return [None]
        elif isinstance(value, list):
            return [[], None]
        elif isinstance(value, tuple):
            return [(), None]
        elif isinstance(value, dict):
            return [{}, None]
        else:
            return [None]

    @classmethod
    def get_random_value(cls, value, max_number=None):
        """
        构造随机数据
        max_number :int 最大随机值
        """
        if isinstance(value, str):
            if max_number is not None:
                return cls.generate_random_str(max_number)
            return cls.generate_random_str(8)
        elif isinstance(value, int):
            if max_number is not None:
                return random.randint(1, max_number)
            return random.randint(1, 100000)
        else:
            return None

    @classmethod
    def get_other_type_list(cls, value):
        """
        构造不正确的value类型
        """
        if isinstance(value, str):
            return [1, ["str"], {"str": "str"}]
        elif isinstance(value, int):
            return [str(value), ["1"], {"int": 1}]
        elif isinstance(value, list):
            return [str(value), 1, {"list": ["list"]}]
        elif isinstance(value, tuple):
            return [str(value), 1, {"tuple": ["tuple"]}]
        elif isinstance(value, dict):
            return [str(value), 1, [{"dict": "dict"}]]
        else:
            return [None]

    @classmethod
    def get_paths(cls, source):
        """
        遍历json，获取所有key路径list
        :param source:
        :return:
        """
        paths = []
        if isinstance(source, collections.abc.MutableMapping):  # found a dict-like structure...
            for k, v in source.items():  # iterate over it; Python 2.x: source.iteritems()
                paths.append([k])  # add the current child path
                paths += [[k] + x for x in cls.get_paths(v)]  # get sub-paths, extend with the current
        elif isinstance(source, collections.abc.Sequence) and not isinstance(source, str):
            for i, v in enumerate(source):
                paths.append([i])
                paths += [[i] + x for x in cls.get_paths(v)]  # get sub-paths, extend with the current
        return paths

    @classmethod
    def get_json_value(cls, json_data, p_l):
        """
        根据key路径list，获取值
        :param json_data: 原始json
        :param p_l: key路径列表
        :return:
        """
        path_str = ""
        for k in p_l:
            if isinstance(k, str):
                path_str += "['" + k + "']"
            if isinstance(k, int):
                path_str += "[" + str(k) + "]"
        return path_str, eval("json_data" + path_str)

    @classmethod
    def set_json_value(cls, json_data, p_l, v):
        """
        根据key路径list，更新值为v
        :param json_data: 原始json
        :param p_l: key路径列表
        :param v: 更新的值
        :return: key路径，更新后的json
        """
        update_json = copy.deepcopy(json_data)
        path_str = ""
        for k in p_l:
            if isinstance(k, str):
                path_str += "['" + k + "']"
            if isinstance(k, int):
                path_str += "[" + str(k) + "]"
        exec("update_json" + path_str + " = v")
        return path_str, update_json

    @classmethod
    def del_json_value(cls, json_data, p_l):
        """
        根据key路径list，删除key
        :param json_data: 原始json
        :param p_l: key路径列表
        :return:
        """
        update_json = copy.deepcopy(json_data)
        path_str = ""
        for k in p_l:
            if isinstance(k, str):
                path_str += "['" + k + "']"
            if isinstance(k, int):
                path_str += "[" + str(k) + "]"
        exec("del update_json" + path_str)
        return path_str, update_json

    @classmethod
    def update_json_data_unique(cls, json_data, p_l):
        """
        根据key路径list，随机生成值
        :param json_data: 原始json
        :param p_l: key路径列表
        :return: key路径，更新后的json
        """
        update_json = copy.deepcopy(json_data)
        path_str = ""
        for k in p_l:
            if isinstance(k, str):
                path_str += "['" + k + "']"
                v = cls.generate_random_str(10)
            if isinstance(k, int):
                path_str += "[" + str(k) + "]"
                v = random.randint(0, 900000)
        exec("update_json" + path_str + " = v")
        return update_json

    @classmethod
    def get_test_data(cls, json_data, path_list, required_flag=""):
        """
        获取测试数据，1、参数缺失，2、参数为空，3、参数类型异常
        :param json_data: 原始json
        :param path_list: key路径列表
        :param required_flag: key是否是必填项
        :return:
        """
        data_update = copy.deepcopy(json_data)
        default_key = "info"
        if default_key in data_update:
            default_key = "exception_situation"
        if required_flag is True:
            required_flag_str = "必填项"
        elif required_flag is False:
            required_flag_str = "非必填项"
        else:
            required_flag_str = ""

        test_param_list = list()
        path_str, value = cls.get_json_value(data_update, path_list)
        path_str, update_json = cls.del_json_value(data_update, path_list)
        copy_test_param = copy.deepcopy(update_json)
        copy_test_param[default_key] = required_flag_str + '参数缺失: ' + path_str
        test_param_list.append(copy_test_param)
        null_value_list = cls.get_null_value_list(value)
        for n in null_value_list:
            path_str, update_json = cls.set_json_value(data_update, path_list, n)
            copy_test_param = copy.deepcopy(update_json)
            if n is None:
                copy_test_param[default_key] = required_flag_str + '参数值为null: ' + path_str
            else:
                copy_test_param[default_key] = required_flag_str + '参数值为空: ' + path_str
            test_param_list.append(copy_test_param)

        r = cls.get_random_value(value)
        if r:
            path_str, update_json = cls.set_json_value(data_update, path_list, r)
            copy_test_param = copy.deepcopy(update_json)
            copy_test_param[default_key] = required_flag_str + '参数值随机: ' + path_str
            test_param_list.append(copy_test_param)

        error_type_list = cls.get_other_type_list(value)
        error_count = 0
        for e in error_type_list:
            error_count += 1
            path_str, update_json = cls.set_json_value(data_update, path_list, e)
            copy_test_param = copy.deepcopy(update_json)
            copy_test_param[default_key] = '参数类型异常' + str(error_count) + ': ' + path_str
            test_param_list.append(copy_test_param)
        return test_param_list

    @classmethod
    def get_test_headers_data(cls, json_data, path_list, required_flag=""):
        """
        获取头部测试数据，1、参数缺失，2、参数为空，3、参数值随机
        :param json_data: 原始json
        :param path_list: key路径列表
        :param required_flag: key是否是必填项
        :return:
        """
        data_update = copy.deepcopy(json_data)
        default_key = "info"
        if default_key in data_update:
            default_key = "exception_situation"
        if required_flag is True:
            required_flag_str = "必填项"
        elif required_flag is False:
            required_flag_str = "非必填项"
        else:
            required_flag_str = ""

        test_param_list = list()
        path_str, value = cls.get_json_value(data_update, path_list)
        path_str, update_json = cls.del_json_value(data_update, path_list)
        copy_test_param = copy.deepcopy(update_json)
        copy_test_param[default_key] = required_flag_str + '参数缺失: ' + path_str
        test_param_list.append(copy_test_param)

        path_str, update_json = cls.set_json_value(data_update, path_list, "")
        copy_test_param = copy.deepcopy(update_json)
        copy_test_param[default_key] = required_flag_str + '参数值为空: ' + path_str
        test_param_list.append(copy_test_param)

        r = cls.get_random_value(value)
        if r:
            path_str, update_json = cls.set_json_value(data_update, path_list, r)
            copy_test_param = copy.deepcopy(update_json)
            copy_test_param[default_key] = required_flag_str + '参数值随机: ' + path_str
            test_param_list.append(copy_test_param)

        return test_param_list

    @classmethod
    def split_path_str(cls, path_str):
        """
        切分路径字符串
        :param path_str:
        :return:
        """
        path_list = path_str.split(".")
        for path_index in range(len(path_list)):
            # noinspection PyBroadException
            try:
                path_list[path_index] = int(path_list[path_index])
            except Exception:
                pass
        return path_list

    @classmethod
    def get_all_exception_test_data(cls, data):
        """
        生成接口参数异常测试用例
        :param data:
        :return:
        """
        exception_data = []
        # 遍历每个参数
        for i in cls.get_paths(data):
            # 遍历到列表类型的参数里面的元素时如不需要处理参数则跳过
            # skip_dict标记列表里的字典key是否跳过（列表里为字典时，只取第一个字段的参数遍历）
            skip_dict = False
            for path_param in i:
                if isinstance(path_param, int):
                    if path_param > 0:
                        skip_dict = True
                        break
            if skip_dict:
                continue

            data_list = cls.get_test_data(data, i)
            for d in data_list:
                exception_data.append(d)
        return exception_data

    @classmethod
    def get_all_exception_test_headers_data(cls, data):
        """
        生成接口头部参数异常测试用例
        :param data:
        :return:
        """

        exception_data = []
        # 遍历每个参数
        for i in cls.get_paths(data):
            # 遍历到列表类型的参数里面的元素时如不需要处理参数则跳过
            # skip_dict标记列表里的字典key是否跳过（列表里为字典时，只取第一个字段的参数遍历）
            skip_dict = False
            for path_param in i:
                if isinstance(path_param, int):
                    if path_param > 0:
                        skip_dict = True
                        break
            if skip_dict:
                continue

            data_list = cls.get_test_headers_data(data, i)
            for d in data_list:
                exception_data.append(d)
        return exception_data

    @classmethod
    def get_str_uuid(cls, random_length=32):
        """
        :param random_length: max  length  32
        :return:
        """
        return str(uuid.uuid4()).replace("-", "")[:random_length]


if __name__ == '__main__':
    print(GetTestParams.get_str_uuid())
    # exception_create_data = GetTestParams.get_all_exception_test_data(
    #     {
    #         "game_id": 104,
    #         "data": {
    #             "action": "modify_name",
    #             "module": "role",
    #             "logical_region_id": 1010,
    #             "server_id": 1,
    #             "show_id": 1008732,
    #             "nick_name": "generate_random_str(5)",
    #             "reason": "测试"
    #         }
    #     })
    # print(exception_create_data)

    # exception_create_data = GetTestParams.get_all_exception_test_headers_data(
    #     {
    #         "action1": "modify_name",
    #         "action2": "modify_name"
    #     })
    # for e in exception_create_data:
    #     print(e)
