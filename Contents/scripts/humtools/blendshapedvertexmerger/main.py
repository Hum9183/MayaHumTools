# -*- coding: utf-8 -*-

from maya import cmds

from ..unexpected_error import UnexpectedError
from .const import Const
from . import selected_getter
from . import blendshape_target_rebuilder
from . import vtx_merger
from . import non_deformer_history_deleter


@UnexpectedError.catch
def main():
    vtx_ids, base_mesh = selected_getter.get_vtx_ids_and_mesh()

    blendshape_targets = blendshape_target_rebuilder.rebuild(base_mesh)

    vtx_merger.merge(vtx_ids, base_mesh)
    non_deformer_history_deleter.delete(base_mesh)

    vtx_merger.merge(vtx_ids, blendshape_targets)
    non_deformer_history_deleter.delete(blendshape_targets)

    '''
    TODO:
    Maya2022ではBaseMeshのnonDeformerHistoryを削除した時点でTargetMeshが壊れてしまう。
    BlendShape自体は削除してしまい、あとでBlendShapeを再設定する方針ならMaya2022でも正常動作しそう。
    '''
