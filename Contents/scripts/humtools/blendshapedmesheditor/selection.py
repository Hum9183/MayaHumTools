# -*- coding: utf-8 -*-
from maya import cmds

from ..util.node_type import NodeType
from ..util.unexpected_error import UnexpectedError


def get_mesh():
    sels = cmds.ls(sl=True)
    __exists_validate(sels)
    __onlyone_validate(sels)
    shape = __to_shape_validate(sels[0])
    __is_mesh_validate(shape)
    return shape


def __onlyone_validate(sels):
    if len(sels) >= 2:
        raise UnexpectedError(u'メッシュを1つのみ選択してください。')


def __to_shape_validate(sel):
    shape = cmds.listRelatives(sel, s=True)[0]
    if shape is None:
        raise UnexpectedError(u'メッシュを選択してください。')
    return shape


def __exists_validate(sels):
    if sels == []:
        raise UnexpectedError(u'メッシュを選択してください。')


def __is_mesh_validate(shape):
    # NOTE: カメラ等ではないかの確認
    if cmds.nodeType(shape) != NodeType.MESH:
        raise UnexpectedError(u'メッシュを選択してください。')
