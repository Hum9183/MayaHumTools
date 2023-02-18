# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from maya import cmds
from maya.common.ui import LayoutManager


class HumWindowBase:
    __metaclass__ = ABCMeta

    def __init__(self, tool_name):
        self.tool_name = tool_name

    def show(self):
        self.__delete_window()
        self._create_window()
        cmds.showWindow()

    @abstractmethod
    def _create_window(self):
        pass

    def __delete_window(self):
        if cmds.window(self.tool_name, ex=True):
            cmds.deleteUI(self.tool_name)
