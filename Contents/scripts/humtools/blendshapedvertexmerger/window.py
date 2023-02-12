# -*- coding: utf-8 -*-
from maya import cmds
from maya.common.ui import LayoutManager

from . import main


class Window:
    def __init__(self, tool_name):
        self.tool_name = tool_name


    def show(self):
        self.__delete_window()
        self.__create_window()
        cmds.showWindow()


    def __delete_window(self):
        if cmds.window(self.tool_name, ex=True):
            cmds.deleteUI(self.tool_name)


    def __create_window(self):
        cmds.window(self.tool_name, title=self.tool_name)
        with LayoutManager(cmds.columnLayout(adj=True)):
            cmds.text(l="")
            cmds.button(l="Merge vertex", h=50,
                        c=lambda args: self.__merge_vertex())
            cmds.text(l="")


    def __merge_vertex(self):
        main.main()