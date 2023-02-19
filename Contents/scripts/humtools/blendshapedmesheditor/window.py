# -*- coding: utf-8 -*-
from maya import cmds
from maya.common.ui import LayoutManager

from ..util.hum_window_base import HumWindowBase
from ..util import in_view_message
from ..util.unexpected_error import UnexpectedError
from .const import Const
from . import cv_freezer
from . import rebuilt_target_mesh_deleter


class Window(HumWindowBase):
    def __init__(self, tool_name):
        super(Window, self).__init__(tool_name)
        self.__editable = False

    def _create_window(self):
        cmds.window(self.tool_name, title=self.tool_name, mxb=False, mnb=False)
        with LayoutManager(cmds.columnLayout(adj=True)):
            cmds.text(l='')
            cmds.button(Const.RUN_BUTTON,
                        l=Const.START_TEXT,
                        ann=Const.START_TEXT,
                        bgc=Const.START_COLOR,
                        c=lambda arg: self.__main())
            cmds.text(l='')

    def __toggle_editable(self, editable, label, annotation, color):
        self.__editable = editable
        cmds.button(Const.RUN_BUTTON, e=True, l=label, ann=annotation, bgc=color)

    @UnexpectedError.catch
    def __start(self):
        rebuilt_target_mesh_deleter.delete()
        self.__toggle_editable(True, Const.FINISH_TEXT, Const.FINISH_ANNOTATION, Const.FINISH_COLOR)
        msg = u'コンポーネント移動・マルチカット編集が可能です'
        in_view_message.show(msg, fadeStayTime=5000)

    @UnexpectedError.catch
    def __finish(self):
        cv_freezer.freeze()
        self.__toggle_editable(False, Const.START_TEXT, Const.START_ANNOTATION, Const.START_COLOR)
        msg = u'コンポーネント移動・マルチカットの編集が不可になりました。'
        in_view_message.show(msg, fadeStayTime=5000)

    def __main(self):
        self.__finish() if self.__editable else self.__start()
