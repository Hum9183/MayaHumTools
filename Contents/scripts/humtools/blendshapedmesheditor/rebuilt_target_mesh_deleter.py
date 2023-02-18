# -*- coding: utf-8 -*-
from maya import cmds

from ..lib import blendshape
from ..util.log import Log
from ..util.selection_recorder import SelectionRecorder
from . import selection
from . import tweak_helper


@SelectionRecorder.record
def delete():
    mesh = selection.get_mesh()
    bs_nodes = blendshape.get_nodes(mesh, raise_ex_if_is_none=True)
    blendshape.delete_rebuilt_target_meshes(bs_nodes)
    tweak_helper.add(mesh)
    Log.log(u'ターゲットメッシュを削除しました')
