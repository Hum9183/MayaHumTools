# -*- coding: utf-8 -*-
from maya import cmds
from maya.common.ui import LayoutManager

from ..const import Const as RootConst
from .const import Const
from . import main


class Window: # TODO: 抽象クラスを作る
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
            cmds.text(l='')
            cmds.button(l='Merge vertex', h=50,
                        c=lambda args: self.__merge_vertex())
            cmds.text(l='')
            self.__create_check_box()


    def __create_check_box(self):
        # NOTE: Maya2022以降はブレンドシェイプを再構築しないとメッシュが壊れる可能性が高い
        recommended_version = RootConst.is_the_maya_version_after_2022()
        cmds.checkBox(Const.RECONFIGURE_BS_CHECK_BOX, l=u'ブレンドシェイプを再構築する', v=recommended_version)


    def __merge_vertex(self):
        reconfigure_bs_setting = cmds.checkBox(Const.RECONFIGURE_BS_CHECK_BOX, q=True, v=True)
        main.main(reconfigure_bs_setting)