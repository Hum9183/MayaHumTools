# -*- coding: utf-8 -*-
from textwrap import dedent

from maya import cmds
from .hum_tools_const import HumToolsConst


def add(tool_name, startup_command_str):
    cmds.menuItem(
        tool_name,
        label=tool_name,
        annotation='Run {}'.format(tool_name),
        parent=HumToolsConst.HUM_TOOLS_FOLDER,
        echoCommand=True,
        command=dedent(startup_command_str)
    )
