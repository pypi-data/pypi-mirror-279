#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/8/13
# @Author  : zxp

import logging


class Log(object):
    def __init__(self, file_path=None, logger_name=None, level='DEBUG', mode='a'):
        """
        :param file_path: 日志文件路径，不传则不保存
        :param level: 日志等级
        """
        super().__init__()
        self.__file_path = file_path
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)
        self.stream_handler = logging.StreamHandler()
        if self.__file_path is not None:
            self.log_file = logging.FileHandler(self.__file_path, mode, encoding='utf-8')

    def logger_init(self):
        formatter = logging.Formatter("%(asctime)s -> %(levelname)s: %(message)s")
        self.stream_handler.setFormatter(formatter)
        self.logger.addHandler(self.stream_handler)
        if self.__file_path is not None:
            self.log_file.setFormatter(formatter)
            self.logger.addHandler(self.log_file)
            self.log_file.close()
        self.stream_handler.close()
        return self.logger
