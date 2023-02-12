# -*- coding: utf-8 -*-
from maya import cmds, mel

from .const import Const


def merge(vtx_ids, meshes):
    if (type(meshes) is list):
        [__merge(vtx_ids, m) for m in meshes]
    else:
        __merge(vtx_ids, meshes)


def __merge(vtx_ids, mesh):
    attr_strs = ['{}.vtx[{}]'.format(mesh, vtx_id) for vtx_id in vtx_ids]
    cmds.select(attr_strs)
    mel.eval('polyMergeToCenter')
    cmds.select(cl=True)