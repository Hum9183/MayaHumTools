# -*- coding: utf-8 -*-
import inspect
from textwrap import dedent

from maya import cmds


def metaclass(class_name):
    """Typeのインスタンスを返す。
    metaclassをpy2でもpy3でも使うためにこのかたちになっている
    https://astropengu.in/posts/32/
    """
    return ReadonlyMeta(
        class_name,
        (object, ),
        {'__doc__': ReadonlyMeta.__doc__})


class RebindError(Exception):
    pass


class ReadonlyMeta(type):
    def __setattr__(self, name, value):
        if name in self.__dict__.keys():
            file_name = get_file_name(inspect.stack())
            func_name = get_func_name(inspect.stack())
            raise RebindError(get_waring_str(
                file_name, func_name, name, value))
        else:
            self.__dict__[name] = value


def get_file_name(stack_records):
    if int(cmds.about(v=True)) >= 2022:  # NOTE: 循環参照回避のためConstのメソッドは使わない
        return stack_records[1].filename
    else:
        return stack_records[1][1]


def get_func_name(stack_records):
    if int(cmds.about(v=True)) >= 2022:
        return stack_records[1].function
    else:
        return stack_records[1][3]


def get_waring_str(file_name, func_name, attr_name, attr_value):
    return u'再代入例外' + dedent(
        u"""
            # 再代入例外: ReadonlyMeta使用しているクラスはアトリビュートに再代入できません。
            # Info:
            #   ファイル...'{}' 
            #   関数...'{}' 
            #   アトリビュート...'{}' 
            #   再代入しようとした値...'{}'
            //////////////////// Rebind Error ///////////////////////
            // Classes using ReadonlyMeta cannot rebind attribute. //
            /////////////////////////////////////////////////////////
        """.format(file_name, func_name, attr_name, attr_value))
