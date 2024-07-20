# -*- coding: utf-8 -*-

from . import non_deformer_history_deleter
from . import selection
from . import tweak_helper
from . import uv_shifter
from ..util.log import Log
from ..util.selection_recorder import SelectionRecorder


@SelectionRecorder.record
def freeze():
    mesh = selection.get_mesh()
    uv_shifter.move_and_restore(mesh)
    non_deformer_history_deleter.delete(mesh)
    tweak_helper.delete(mesh)
    Log.log(u'CVをフリーズしました。')
