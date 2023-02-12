# -*- coding: utf-8 -*-
from maya import cmds, mel
from .const import Const

def delete(meshes):
    if (type(meshes) is list):
        [__delete(m) for m in meshes]
        return
    else:
        __delete(meshes)


def __delete(mesh):
    cmds.select(mesh)
    mel.eval('BakeNonDefHistory')
    cmds.select(cl=True)