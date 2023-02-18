# -*- coding: utf-8 -*-
from maya import cmds

from .util.readonly import metaclass


class Const(metaclass('Const')):
    HUM_TOOLS_FOLDER = 'HumToolsFolder'
    HUM_TOOLS        = 'HumTools'
    MAYA_VERSION     = int(cmds.about(v=True))

    @staticmethod
    def is_the_maya_version_after_2022():
        return Const.MAYA_VERSION >= 2022

    @staticmethod
    def is_the_maya_version_before_2020():
        return Const.MAYA_VERSION <= 2020