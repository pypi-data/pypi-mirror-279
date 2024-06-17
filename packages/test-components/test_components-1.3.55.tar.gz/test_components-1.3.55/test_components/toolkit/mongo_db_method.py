#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# @Time    : 2024/5/21 14:22:52
# @Author  : zxp

import pymongo, configparser, os


class MongoDB:
    """
    目前配置固定字段 section 读取 mongodb， option 读取db_url，以后可以会有额外的固定字段，所以option字段用列表存储
    """

    mongodb = 'mongodb'
    db_info_list = ['db_url']

    def db_connect(self, file_path):
        """
        连接mongo数据库
        :param file_path: 文件配置路径
        :return:
        """

        if os.path.exists(file_path):
            conf = configparser.ConfigParser()
            conf.read(file_path, encoding="utf-8")

            if self.mongodb not in conf.sections():
                raise configparser.NoSectionError('没有[mongodb]的配置')
            for info in self.db_info_list:
                if info not in conf.options(self.mongodb):
                    raise NameError('配置文件缺失key值：' + info)

            self.db_url = conf.get('mongodb', 'db_url')
            self.mongo_client = pymongo.MongoClient(self.db_url)
        else:
            raise ValueError("配置路径不存在\n" + file_path)

    def db_find(self, db_name, table_name, find_obj):
        """
        查找 mongo数据库表中的数据
        :param db_name: 数据库名
        :param table_name: 表名
        :param find_obj: 查询条件
        :return:
        """

        order = self.mongo_client[db_name][table_name]
        find_result = order.count_documents(find_obj)
        if find_result != 0:
            return find_result, order.find(find_obj)
        else:
            return find_result, [None]

    def db_insert(self, db_name, table_name, insert_obj):
        """
        向mongo数据库表插入数据
        :param db_name: 数据库名
        :param table_name: 表名
        :param insert_obj: 插入数据
        :return:
        """

        order = self.mongo_client[db_name][table_name]
        order.insert_one(insert_obj)

    def db_del(self, db_name, table_name, find_obj):
        """
        删除mongo数据库表中的数据
        :param db_name: 数据库名
        :param table_name: 表名
        :param find_obj: 查询条件
        :return:
        """

        order = self.mongo_client[db_name][table_name]
        order.delete_one(find_obj)

    def db_update(self, db_name, table_name, find_obj, update_obj):
        """
        更新mongo数据库表中的数据
        :param db_name: 数据库名
        :param table_name: 表名
        :param find_obj: 查询条件
        :param update_obj: 更新字段
        :return:
        """

        order = self.mongo_client[db_name][table_name]
        order.update_one(find_obj, {"$set": update_obj})

    def db_close(self):
        self.mongo_client.close()
