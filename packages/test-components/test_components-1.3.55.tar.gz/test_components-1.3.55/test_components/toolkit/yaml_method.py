#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2021/01/14
# @Author  : zxp
import yaml


class YamlMethod(object):
    @classmethod
    def yaml_r(cls, yamlPath):
        """
        读取yaml文件
        :param yamlPath:文件路径
        :return:
        """
        with open(yamlPath, 'r', encoding='utf-8') as f:
            result = f.read()
            data = yaml.load(result)
            return data

    @classmethod
    def yaml_w(cls, yamlPath, data):
        with open(yamlPath, "w", encoding="utf-8") as f:
            yaml.dump(data, f)






