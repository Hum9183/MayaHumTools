# -*- coding: utf-8 -*-
from maya import cmds

from ..const import Const


class Log:
    @staticmethod
    def log(message):
        print(u'{} : {}'.format(Const.HUM_TOOLS, message))

    @staticmethod
    def warning(message):
        cmds.warning(u'{} : {}'.format(Const.HUM_TOOLS, message))

    @staticmethod
    def error(message):
        cmds.error(u'{} : {}'.format(Const.HUM_TOOLS, message))