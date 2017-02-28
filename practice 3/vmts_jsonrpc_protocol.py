# -*- coding: utf-8 -*-

import time
import json

from vmts_pre_define import pre_init
from vmts_logger import VmtsLogger
from vmts_exceptions import RpcValidationError, LackParameterError, TransformJsonError


def gen_id(dev_id=None):
    """
    Function for generating post id.
    :param dev_id: default is None.
    :return: <string> id string.
    """

    if dev_id is None:
        dev_id = pre_init().get_module('vmts_conf').device.dev_id
    return dev_id + '-' + str(time.time()).replace('.', '')


def check_recv(func):
    """
    Decorator for validating received post.
    :param func: function object which is decorated.
    :return: call <func> _deco, to check the received post.
    """
    def _deco(self, recv):
        """
        Decorator function, will capture the received post, and verify its format.
        :param self: the instance of Decorated class.
        :param recv: the received post.
        :return: call <func> func
        """

        VmtsLogger('rpc_protocol').debug("self:{self}; recv:{recv}; func:{func} in decorator check_recv".format(
            self=self, recv=recv, func=func.__name__))

        def check_key(key_lst, src_dict):
            """
            Function to check that keys of one dict <src_dict> are all included in the list
            <key_lst> or not.
            :param key_lst: <list>, src key list.
            :param src_dict: <dict>, src dict.
            :return: <bool>.
            """

            l = len(key_lst)
            tmp = 0
            for i in src_dict:
                if i not in key_lst:
                    return False
                else:
                    key_lst.pop(i)
                    tmp += 1

            if tmp == l:
                return True
            else:
                return False

        try:
            recv_json = json.loads(recv)
        except ValueError:
            raise TransformJsonError
        try:
            src_list = ['id', 'method', 'params'] if self._type == 'request' else \
                ['id', 'result', 'error']

            if self._type not in ['request', 'response']:
                raise RpcValidationError('Wrong protocol type')

            if not check_key(src_list, recv_json):
                raise RpcValidationError('Bad protocol field')

            return func(self, recv_json)
        except IndexError:
            raise LackParameterError
    return _deco


def check_args(func):
    """
    Decorator for validating post.
    :param func: function object which is decorated.
    :return: call <func> _deco, to check the received post.
    """

    def _deco(self, *args, **argv):
        """
        Decorator function, will capture post, and verify its format.
        :param self: the instance of Decorated class.
        :param args: <list>, parameters.
        :param argv: <dict>, parameters.
        :return: call <func> func
        """
        VmtsLogger('rpc_protocol').debug("self:{self}; args:{args}; func:{func} in decorator check_args".format(
            self=self, args=args, func=func.__name__))
        try:
            if self._type == 'request':
                if len(args) + len(argv) == 2:
                    return func(self, args, argv)
            elif self._type == 'response':
                if len(args) + len(argv) == 3:
                    return func(self, args, argv)
            else:
                raise LackParameterError
        except IndexError:
            raise LackParameterError
    return _deco


class WebsocketJsonRpcProtocolConstructor(object):
    """
    with WebsocketProtocolConstructor(uid, _type) as ins:
            do something

        when exit <with> statments, del the WebsocketProtocol instance.
    """

    version = '1.0.0'

    def __init__(self, _type):

        self.instance = WebsocketJsonRpcProtocol(_type=_type)

    def __enter__(self):
        """
        overload __enter__ method.
        return WebsocketProtocol instance.
        :return: <object>.
        """

        return self.instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        overload __exit__ method.
        :return: None.
        """
        if exc_type is None:
            del self.instance
        else:
            VmtsLogger('rpc_protocol').debug("__exit__ {type}: {val}\n\t{tb}".format(
                type=exc_type, val=exc_val, tb=exc_tb
            ))


class WebsocketJsonRpcProtocol(object):
    """
    Definition of Json-rpc protocol structure.
    """

    version = '1.0.0'

    def __init__(self, _type):

        self._type = _type.lower()

        if self._type != 'request' and self._type != 'response':
            raise Exception('Wrong protocol type, "request" or "response" expected. '
                            'Got {err_type}.'.format(err_type=self._type))
        if self._type == 'request':
            self.uid = gen_id()
            self.pack = self.__request_pack
            self.unpack = self.__request_unpack
        elif self._type == 'response':
            self.uid = None
            self.pack = self.__response_pack
            self.unpack = self.__response_unpack

    @check_args
    def __request_pack(self, method, params):

        if not params:
            params = {}

        return json.dumps(
            {
                "id": self.uid,
                "method": method,
                "params": params
            }
        )

    @check_args
    def __response_pack(self, uid, result, err):

        return json.dumps(
            {
                "id": uid,
                "result": result,
                "error": err
            }
        )

    @check_recv
    def __request_unpack(self, recv):

        return recv['id'], recv['method'], recv['params']

    @check_recv
    def __response_unpack(self, recv):

        return recv['id'], recv['result'], recv['error']

    @staticmethod
    def _ver():
        return WebsocketJsonRpcProtocol.version
