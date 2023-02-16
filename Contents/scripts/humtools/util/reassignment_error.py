# -*- coding: utf-8 -*-
from textwrap import dedent
import traceback


class ReassignmentError(Exception):
    def __init__(self, attr_name, attr_value, class_name):
        self.__attr_name = attr_name
        self.__attr_value = attr_value
        self.__class_name = class_name

    def log(self):
        print(traceback.format_exc())
        message=dedent(
            u"""
                # 再代入例外: ReadonlyAttrを継承しているクラスはアトリビュートに再代入できません。
                # Info:
                #   クラス...'{}' 
                #   アトリビュート...'{}' 
                #   再代入しようとした値...'{}'
                ///////////// Re-assignment Error //////////////
                // Classes that inherit from ReadonlyAttr are //
                // Attributes cannot be reassigned.           //
                ////////////////////////////////////////////////
            """.format(self.__class_name, self.__attr_name, self.__attr_value))
        print(message)
