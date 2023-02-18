# -*- coding: utf-8 -*-
from maya import cmds


def move_and_restore(mesh):
    cmds.select('{}.map[0]'.format(mesh), r=True)
    cmds.polyEditUV(u=1)
    cmds.polyEditUV(u=-1)
    cmds.select(cl=True)