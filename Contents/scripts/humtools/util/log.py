# -*- coding: utf-8 -*-
from maya import cmds

from ..hum_tools_const import HumToolsConst


class Log:
    @staticmethod
    def log(message):
        print(u'{} : {}'.format(HumToolsConst.HUM_TOOLS, message))

    @staticmethod
    def warning(message):
        cmds.warning(u'{} : {}'.format(HumToolsConst.HUM_TOOLS, message))

    @staticmethod
    def error(message):
        cmds.error(u'{} : {}'.format(HumToolsConst.HUM_TOOLS, message))