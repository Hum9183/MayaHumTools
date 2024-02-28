# -*- coding: utf-8 -*-
from maya import cmds, mel

from ..hum_tools_const import HumToolsConst
from ..util.node_type import NodeType


def add(mesh):
    if HumToolsConst.is_the_maya_version_before_2020():
        return
    cmds.select(mesh, r=True)
    mel.eval('AddTweak')
    cmds.select(cl=True)


def delete(mesh):
    if HumToolsConst.is_the_maya_version_before_2020():
        return
    tweak = NodeType.get_histories(mesh, NodeType.TWEAK, raise_ex_if_is_none=True)
    cmds.delete(tweak)
