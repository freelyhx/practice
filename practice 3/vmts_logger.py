# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

from vmts_const import pSlash
from vmts_pre_define import pre_init

log_relative_path = '{slash}'.format(slash=pSlash).join(['', '..', 'log', ''])


def singleton(cls, *args, **kw):
    """
    Singleton decorator function.
    :param cls: Class object decorated.
    :param args: optional parameters with a list-like format.
    :param kw: optional parameters with a dict-like format.
    :return: wrap decorated object, and return its self.
    """

    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = {args[0]: cls(*args, **kw)}
        else:
            if args[0] not in instances[cls]:
                instances[cls][args[0]] = cls(*args, **kw)
        return instances[cls][args[0]]
    return _singleton


@singleton
class VmtsLogger(object):
    """
    Vmts logger wrap-class.
    """

    formatter = '%(levelname)s - %(asctime)s %(name)s: %(message)s'
    formmater_debug = '%(levelname)s - %(asctime)s %(name)s: %(message)s\n\tCall Stack Info:\n\t\tfunction: ' \
                      '%(funcName)s\n\t\tmodule: %(module)s\n\t\tfile: %(pathname)s'

    def __init__(self, name, base_dir=os.path.dirname(__file__) + log_relative_path):

        self.pre_conf = pre_init().get_module('vmts_conf')
        self.name = name
        self.fp = base_dir + name + '.log'
        self.debug = self.pre_conf.logger.debug
        self.level = logging.DEBUG if self.debug else logging.INFO
        self.logger = logging.getLogger()
        self.logger.setLevel(self.level)
        self.formatter = VmtsLogger.formatter if not self.debug else VmtsLogger.formmater_debug

        file_handle = logging.handlers.TimedRotatingFileHandler(self.fp, when='D', backupCount=5, encoding='utf-8')
        file_handle.setLevel(self.level)
        console_handle = logging.StreamHandler()
        console_handle.setLevel(self.level)

        self.logger.addHandler(file_handle)
        self.logger.addHandler(console_handle)

    def debug(self, msg):
        """
        wrapper of method 'logger.debug'.
        :param msg: log message.
        :return: None.
        """

        return self.logger.debug(msg)

    def info(self, msg):
        """
        wrapper of method 'logger.info'.
        :param msg: log message.
        :return: None.
        """

        return self.logger.info(msg)

    def warning(self, msg):
        """
        wrapper of method 'logger.warning'.
        :param msg: log message.
        :return: None.
        """

        return self.logger.warning(msg)

    def error(self, msg):
        """
        wrapper of method 'logger.error'.
        :param msg: log message.
        :return: None.
        """

        return self.logger.error(msg)

    def critical(self, msg):
        """
        wrapper of method 'logger.critical'.
        :param msg: log message.
        :return: None.
        """

        return self.logger.critical(msg)


def logger_init():
    """
    Function for vmts-logger singleton instance initialize.
    :return: singleton instance of VmtsLogger class.
    """

    paths = pre_init().get_module('vmts_conf').logger.persistence_path
    for i in paths:
        if paths[i] == '.':
            VmtsLogger(i)
        else:
            # todo: optional log root paths.
            VmtsLogger(i, paths[i])
