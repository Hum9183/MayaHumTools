# -*- coding: utf-8 -*-

class Const:
    HUM_TOOLS_FOLDER = 'HumToolsFolder'
    HUM_TOOLS        = 'HumTools'
    MAYA_VERSION     = 404

    @staticmethod
    def is_the_maya_version_after_2022():
        return Const.MAYA_VERSION >= 2022