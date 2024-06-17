#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/15 16:09
# @Author  : 张晓平
import uuid
import time
import datetime
from datetime import timezone, timedelta
from elasticsearch import Elasticsearch
from .log_method import Log


class Es(Log):
    def __init__(self, index_name, logger_name=None, es_host="", file_path=None, level='INFO',
                 mode='a'):
        super().__init__(file_path, logger_name, level, mode)
        self.log = self.logger_init()
        self.es_host = es_host
        self.index_name = index_name
        try:
            self.es = Elasticsearch(hosts=self.es_host, sniff_on_start=True)
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name, ignore=400)
        except Exception as e:
            print(str(e))

    # 创建索引,ignore=400 容错处理,已创建时,系统不会崩溃
    def create_index_name(self):
        # 创建后需要插入数据,kibana索引才能建立,才有数据
        return self.es.indices.create(index=self.index_name, ignore=400)

    # 插入数据
    def insert_data(self, log_data):
        """
        :param log_data: dict
        :return:
        """
        return self.es.create(index=self.index_name, id=str(uuid.uuid1()).replace("-", ''), document=log_data)

    def es_debug(self, log_data):
        self.logger.debug(log_data)
        self.insert_data(log_data)

    def es_info(self, log_data):
        self.logger.info(log_data)
        self.insert_data(log_data)

    def es_error(self, log_data):
        self.logger.error(log_data, exc_info=True, stack_info=True)
        self.insert_data(log_data)

    def es_warning(self, log_data):
        self.logger.warning(log_data, exc_info=True)
        self.insert_data(log_data)

    def log_format(self, log_out: dict, request=None, response=None, data=None, info=None, msg=None):
        if not isinstance(log_out, dict):
            self.logger.error("error type", exc_info=True, stack_info=True)
            return "error type"
        log_index = {"request": request, "response": response, "data": data, "info": info, "msg": msg}
        for k, y in log_index.items():
            if y:
                log_out[k] = y
        log_out["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        # 必填字段用于时间筛选,带有时区
        log_out["@timestamp"] = datetime.datetime.now(tz=timezone(timedelta(hours=8))).replace()
        return log_out
