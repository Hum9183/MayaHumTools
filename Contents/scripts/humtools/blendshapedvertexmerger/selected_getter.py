# -*- coding: utf-8 -*-
import re

from maya import cmds

from ..util.unexpected_error import UnexpectedError
from .const import Const


def get_vtx_ids_and_mesh():
    sels = cmds.ls(sl=True, flatten=True)

    __exists_validate(sels)

    __only_vtx_validate(sels)

    mesh_name = __get_first_sel_mesh_name(sels)
    __only_one_mesh_validate(sels, mesh_name)

    __multiple_vtx_validate(sels)

    vtx_ids = __get_vtx_ids(sels)

    return vtx_ids, mesh_name


def __exists_validate(sels):
    if (sels == []):
        raise UnexpectedError(u"頂点を選択してください。")


def __only_vtx_validate(sels):
    vtx_comp_str = '.vtx['
    for sel in sels:
        if not vtx_comp_str in sel:
            raise UnexpectedError(u"頂点のみを選択してください。")


def __get_first_sel_mesh_name(sels):
    FIRST_IDX = 0
    return __get_split_by_a_dot(sels[0], FIRST_IDX)


def __only_one_mesh_validate(sels, mesh_name):
    FIRST_IDX = 0
    for sel in sels:
        first_word = __get_split_by_a_dot(sel, FIRST_IDX)
        if first_word != mesh_name:
            raise UnexpectedError(u"一つのメッシュの頂点を選択してください。")


def __get_split_by_a_dot(string, index):
    return string.split('.')[index]


def __multiple_vtx_validate(sels):
    if len(sels) == 1:
        raise UnexpectedError(u"複数の頂点を選択してください")


def __get_vtx_ids(sels):
    END_IDX = 1
    vtx_ids = []
    for sel in sels:
        end_word = __get_split_by_a_dot(sel, END_IDX)
        vtx_ids.append(re.sub(r'\D', '', end_word))
    return vtx_ids
