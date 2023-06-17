# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from maya import cmds


class HumWindowBase:
    """cmdsを用いたGUIウィンドウを使用する場合に継承する基底クラス。"""
    __metaclass__ = ABCMeta

    def __init__(self, tool_name):
        """
        Args:
            tool_name (str): ツール名
        """
        self.tool_name = tool_name

    def show(self):
        """ウィンドウを生成し、表示する"""
        self.__delete_window()
        self._create_window()
        cmds.showWindow()

    def reload_window(self):
        """ウィンドウをリロードする。"""
        cmds.evalDeferred(lambda *args: self.show())

    @abstractmethod
    def _create_window(self):
        """ウィンドウを生成する。
        抽象メソッドであるため、実装はすべて派生クラスに記述する。
        """
        pass

    def __delete_window(self):
        """ウィンドウを削除する。"""
        if cmds.window(self.tool_name, ex=True):
            cmds.deleteUI(self.tool_name)