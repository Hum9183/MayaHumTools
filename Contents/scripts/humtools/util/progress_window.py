# -*- coding: utf-8 -*-
from maya import cmds

from .lang import Lang

class ProgressWindow:
    def __init__(self, maxLoopCount, description, lang):
        if maxLoopCount < 1:
            raise ProgressWindowException(Lang.pack(u'maxLoopCountは1以上を指定してください。', 'maxLoopCount must be at least 1.', lang))
        self.__maxLoopCount = maxLoopCount
        self.__description = description

    def show(self):
        cmds.progressWindow(title="Progress",
                            maxValue=self.__maxLoopCount,
                            status=self.__description,
                            isInterruptable=True)

    def is_cancelled(self):
        isCancelled = cmds.progressWindow(q=True, isCancelled=True)
        return True if isCancelled else False

    def is_greater_than_max(self):
        progressCount = cmds.progressWindow(q=True, progress=True)
        isGreaterThanMax =  progressCount >= self.__maxLoopCount
        return True if isGreaterThanMax else False

    def next(self):
        cmds.progressWindow(e=True, step=1)

    def close(self):
        cmds.progressWindow(endProgress=True)


class ProgressWindowException(Exception):
    pass
