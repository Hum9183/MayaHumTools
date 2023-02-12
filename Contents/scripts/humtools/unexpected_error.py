# -*- coding: utf-8 -*-
import functools

from maya import cmds

from .log import Log


class UnexpectedError(Exception):
    @staticmethod
    def catch(function):
        """UnexpectedErrorを検知するデコレータ"""
        @functools.wraps(function)
        def wrapper(*args, **keywords):
            try:
                returnValue = function(*args, **keywords)
            except UnexpectedError as e:
                e.log()
                return
            return returnValue
        return wrapper

    def log(self):
        self.__output_scripteditor()
        self.__show_inviewmessage()

    def __output_scripteditor(self):
        msg = u"{}".format(self)
        Log.log(msg)

    def __show_inviewmessage(self):
        highlightedMsg = u"<hl>{}</hl>".format(self)
        cmds.inViewMessage(amg=highlightedMsg, pos="botCenter", fade=True)
