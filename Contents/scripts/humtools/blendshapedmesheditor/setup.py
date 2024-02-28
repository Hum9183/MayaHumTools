# -*- coding: utf-8 -*-
import inspect

from maya import cmds

from .. import menu_adder
from .const import Const
from . import startup_command


def add_menu():
    # NOTE: シェルフに登録できるようにするために、起動コマンドはstringで渡す
    startup_command_str = inspect.getsource(startup_command)
    menu_adder.add(Const.TOOL_NAME, startup_command_str)
