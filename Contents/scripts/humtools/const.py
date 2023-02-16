# -*- coding: utf-8 -*-

from maya import cmds


class Const:
    HUM_TOOLS_FOLDER = 'HumToolsFolder'
    HUM_TOOLS        = 'HumTools'
    MAYA_VERSION     = int(cmds.about(v=True))

    @staticmethod
    def is_the_maya_version_after_2022():
        return Const.MAYA_VERSION >= 2022