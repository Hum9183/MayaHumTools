# -*- coding: utf-8 -*-
import functools

from maya import cmds

from ..util.readonly import metaclass


class SelectionRecorder(metaclass('SelectionRecorder')):
    def __init__(self, selections):
        self.__selections = selections

    @staticmethod
    def record(function):
        """選択状態を記憶し元に戻すデコレータ"""
        @functools.wraps(function)
        def wrapper(*args, **keywords):
            sel_rec = SelectionRecorder.__record()
            returnValue = function(*args, **keywords)
            sel_rec.restore()
            return returnValue
        return wrapper

    @staticmethod
    def __record():
        sels = cmds.ls(sl=True)
        return SelectionRecorder(sels)

    def restore(self):
        print(self.__selections)
        cmds.select(self.__selections, r=True)
