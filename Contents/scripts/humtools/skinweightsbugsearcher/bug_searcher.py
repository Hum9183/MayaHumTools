# -*- coding: utf-8 -*-
from maya import cmds, mel

from ..util.lang            import Lang
from ..util.progress_window import ProgressWindow
from ..util.time_recorder   import TimeRecorder
from .lang_op_var           import LangOpVar
from .selection             import Selection
from .working_mesh          import WorkingMesh


@TimeRecorder.wraps
def search():
    selection = Selection()
    sel_list = selection.get_meshes_as_sel_list()

    working_meshes = WorkingMesh.create_from_sel_list(sel_list)

    all_meshes_vert_count = __get_all_meshes_vert_count(working_meshes)
    progress_window = ProgressWindow(all_meshes_vert_count, Lang.pack(u'頂点を走査中', 'Scanning vertex', LangOpVar.get()), LangOpVar.get())
    progress_window.show()

    all_bugs = []
    for working_mesh in working_meshes:
        bugs = __get_bugs(working_mesh, progress_window)
        all_bugs.extend(bugs)

    progress_window.close()
    cmds.select(cl=True)

    return all_bugs


def __get_all_meshes_vert_count(working_meshes):
    vert_count_list = [wm.vert_count for wm in working_meshes]
    return sum(vert_count_list)


def __get_bugs(working_mesh, progress_window):
    bugs = []
    while not working_mesh.mesh_vert_it_main.isDone():
        if progress_window.is_cancelled():
            break
        progress_window.next()

        nearby_vert_ids = working_mesh.get_vert_ids_nearby_current_vert()
        nearby_vert_infl_valid = working_mesh.calc_infl_vaild_nearby_verts(nearby_vert_ids)

        skin_weights = working_mesh.get_current_vert_skinweights()
        infl_names = working_mesh.calc_unexpected_influeces(skin_weights, nearby_vert_infl_valid)

        if infl_names != []:
            vert_id = working_mesh.get_current_vert_id()
            joined_infl_name = '@'.join(infl_names)
            item_name = '{}.vtx[{}]@{}'.format(working_mesh.name, vert_id, joined_infl_name)
            bugs.append(item_name)

        working_mesh.mesh_vert_it_main.next()

    return bugs
