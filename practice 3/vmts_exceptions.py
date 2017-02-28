# -*- coding: utf-8 -*-


from vmts_logger import VmtsLogger
from vmts_pre_define import pre_init

config = pre_init().get_module('vmts_conf')


class VmtsExceptions(Exception):
    """
    Base class of vmts exceptions.
    """

    def __init__(self, msg):
        VmtsLogger('error').error(msg)


class RpcValidationError(VmtsExceptions):
    """
    json-rpc protocol validation error.
    will be raised when found errors on protocol structure.
    """

    def __init__(self, msg):
        self.msg = msg
        super(RpcValidationError, self).__init__(self.msg)


class LackParameterError(VmtsExceptions):
    """
    json-rpc protocol construction error.
    will be raised when number of parameters isn`t right.
    """

    def __init__(self):
        self.msg = 'Lack of parameter for constructing protocol.'
        super(LackParameterError, self).__init__(self.msg)


class TransformJsonError(VmtsExceptions):
    """
    json-rpc protocol construction error.
    will be raised when json-string cannot be resolved.
    """

    def __init__(self):
        self.msg = 'Unable to transform json-string into python-dict.'
        super(TransformJsonError, self).__init__(self.msg)
