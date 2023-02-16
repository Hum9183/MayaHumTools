# -*- coding: utf-8 -*-
from textwrap import dedent

from maya import cmds
from .const import Const


def add(tool_name, startup_command_str):
    cmds.menuItem(
        tool_name,
        label=tool_name,
        annotation='Run {}'.format(tool_name),
        parent=Const.HUM_TOOLS_FOLDER,
        echoCommand=True,
        command=dedent(startup_command_str)
    )
