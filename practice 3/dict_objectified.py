# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-10-24 11:26:15
# @Last Modified by:   hylide
# @Last Modified time: 2016-10-24 11:26:36


class DictObject(object):

    def __init__(self, dict_obj):

        self.keys = dict_obj.keys()
        for i in self.keys:
            if type(dict_obj[i]) == dict:
                self.__setattr__(i,  DictObject(dict_obj[i]))
            else:
                self.__setattr__(i, dict_obj[i])

    def __repr__(self):
        """
        overload __builtin__ method: __repr__
        """

        return self.__dictionary__()

    def __str__(self):
        """
        overload __builtin__ method: __str__
        """

        return str(self.__repr__())

    def __getitem__(self, item):
        """
        overload __builtin__ method: __getitem__
        :param item: the key of which item`s value you wanna to get.
        :return: value of attribute.
        """

        if isinstance(self.__getattribute__(item), DictObject):
            return self.__getattribute__(item).__str__()
        else:
            return self.__getattribute__(item)

    def __dictionary__(self):
        """
        overload __builtin__ method: __dictionary__
        :return: list with attr-names of the DictObject tree
        """

        attr = self.__dict__
        for i in attr.keys():
            if isinstance(attr[i], DictObject):
                attr[i] = attr[i].__dictionary__()
        return attr

    def keys(self):
        """
        :return: <list>, set with all keys.
        """

        return self.__dict__.keys()

    def has_key(self, key):
        """
        overload dict`s has_key method.
        :param key: input key.
        :return: <boolean>
        """

        if key in self.__dict__.keys():
            return True
        else:
            return False

    def dumps(self):
        """
        method for dumpping DictObject instance to a Dictionary-Object.
        :return: <dict>
        """

        tmp = dict()
        for i in self.keys:
            value = self.__getattribute__(i)
            if isinstance(value, DictObject):
                tmp[i] = value.dumps()
            else:
                tmp[i] = value
        return tmp
