# -*- coding: utf-8 -*-
from maya import cmds, mel


def delete(meshes):
    if (type(meshes) is list):
        [__delete(m) for m in meshes]
    else:
        __delete(meshes)


def __delete(mesh):
    cmds.select(mesh)
    mel.eval('BakeNonDefHistory')
    cmds.select(cl=True)