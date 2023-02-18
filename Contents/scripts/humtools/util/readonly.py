# -*- coding: utf-8 -*-
import inspect
from textwrap import dedent

from maya import cmds


class RebindError(Exception):
    pass


class ReadonlyMeta(type):
    def __setattr__(self, name, value):
        if name in self.__dict__.keys():
            file_name = ''
            func_name = ''
            if int(cmds.about(v=True)) >= 2022:  # NOTE: 循環参照回避のためConstのメソッドは使わない
                file_name = inspect.stack()[1].filename
                func_name = inspect.stack()[1].function
            else:
                file_name = inspect.stack()[1][1]
                func_name = inspect.stack()[1][3]
            raise RebindError(get_waring_str(
                file_name, func_name, name, value))
        else:
            self.__dict__[name] = value


def metaclass(class_name):
    """Typeのインスタンスを返す。
    metaclassをpy2でもpy3でも使うためにこのかたちになっている
    https://astropengu.in/posts/32/
    """
    return ReadonlyMeta(
        class_name,
        (object, ),
        {'__doc__': ReadonlyMeta.__doc__})


def get_waring_str(file_name, func_name, attr_name, attr_value):
    return u'再代入例外' + dedent(
        u"""
            # 再代入例外: Readonlyを継承しているクラスはアトリビュートに再代入できません。
            # Info:
            #   ファイル...'{}' 
            #   関数...'{}' 
            #   アトリビュート...'{}' 
            #   再代入しようとした値...'{}'
            ///////////////////// Rebind Error ///////////////////////
            // Classes inheriting Readonly cannot rebind Attribute. //
            //////////////////////////////////////////////////////////
        """.format(file_name, func_name, attr_name, attr_value))
