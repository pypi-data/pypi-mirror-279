#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2021/03/05
# @Author  : zxp

import pymysql
import os
import configparser


class MysqlDB(object):

    def __init__(self, file_path, port=3306, db_conf="db", config_node="mysqlDB"):
        if os.path.exists(file_path):
            conf = configparser.ConfigParser()
            conf.read(file_path, encoding="utf-8")
        else:
            raise ValueError("配置路径不存在\n" + file_path)
        self.db = pymysql.connect(host=conf.get(config_node, "host"),
                                  user=conf.get(config_node, "user"),
                                  passwd=conf.get(config_node, "pwd"),
                                  db=conf.get(config_node, db_conf),
                                  port=port,
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def db_execute(self, sql_param, args=None):
        if sql_param[0].lower() == "s":
            self.cursor.execute(sql_param, args)
            data = self.cursor.fetchall()

            return data
        elif sql_param[0].lower() == "u" or \
                sql_param[0].lower() == "i" \
                or sql_param[0].lower() == "c" \
                or sql_param[0].lower() == "d":
            result = self.cursor.execute(sql_param, args)
            self.db.commit()
            self.db.rollback()
            return result

    def db_close(self):
        self.cursor.close()
        self.db.close()
