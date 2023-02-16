# -*- coding: utf-8 -*-

from maya import cmds

from ..util.unexpected_error import UnexpectedError
from ..lib import blendshape
from .blendshape_reconfigurator import BlendShapeReconfigurator
from .const import Const
from . import blendshape_target_rebuilder
from . import non_deformer_history_deleter
from . import selected_getter
from . import vtx_merger


@UnexpectedError.catch
def main(reconfigure_bs_setting):
    vtx_ids, base_mesh = selected_getter.get_vtx_ids_and_mesh()

    blendshape_targets = blendshape_target_rebuilder.rebuild(base_mesh)
    bs_reconfigurator = BlendShapeReconfigurator(reconfigure_bs_setting, base_mesh, blendshape.get_nodes(base_mesh))
    bs_reconfigurator.preserve()
    bs_reconfigurator.delete_nodes()

    vtx_merger.merge(vtx_ids, base_mesh)
    non_deformer_history_deleter.delete(base_mesh)

    vtx_merger.merge(vtx_ids, blendshape_targets)
    non_deformer_history_deleter.delete(blendshape_targets)

    bs_reconfigurator.configure()