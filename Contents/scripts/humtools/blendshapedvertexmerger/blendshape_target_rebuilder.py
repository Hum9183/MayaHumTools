# -*- coding: utf-8 -*-
from itertools import chain

from maya import cmds

from ..util.unexpected_error import UnexpectedError
from .const import Const


def rebuild(base_mesh):
    bs_nodes = __get_bs_nodes(base_mesh)

    __exists_validate(bs_nodes)

    rebuilt_targets = [__rebuild(bs) for bs in bs_nodes]
    return list(chain.from_iterable(rebuilt_targets))


def __get_bs_nodes(base_mesh):
    histories = cmds.listHistory(base_mesh)
    BLEND_SHAPE = 'blendShape'
    return cmds.ls(histories, type=BLEND_SHAPE)


def __exists_validate(bs_nodes):
    if bs_nodes == []:
        raise UnexpectedError(u"ブレンドシェイプが存在しません。")


def __rebuild(bs_node):
    target_indices = cmds.getAttr(
        '{}.targetDirectory[0].childIndices'.format(bs_node))
    __set_bs_weight_to_zero(bs_node, target_indices)
    __delete_already_rebuilt_targets(bs_node)
    rebuilt_targets = __create_mesh(bs_node, target_indices)
    __hide(rebuilt_targets)
    return rebuilt_targets


def __set_bs_weight_to_zero(bs_node, bs_targets_indices):
    # NOTE: ブレンドシェイプのウェイト値が入っていると、メッシュが壊れるため、セーフティとして行う
    WEIGHT_VALUE = 0
    for idx in bs_targets_indices:
        cmds.blendShape(bs_node, e=True, weight=(idx, WEIGHT_VALUE))


def __delete_already_rebuilt_targets(bs_node):
    # NOTE: すでにリビルド済みのメッシュはBSノードにコネクトしていてうまくマージできない可能性があるため、一旦すべて削除する
    # NOTE: ターゲット名とリビルド済のターゲットメッシュ名が異なる可能性もあるため、そういう場合のためにも一旦すべて削除する
    rebuilt_target_meshes = cmds.blendShape(bs_node, q=True, t=True)   # WARNING: BS名ではない
    if (rebuilt_target_meshes != []):
        cmds.delete(rebuilt_target_meshes)


def __create_mesh(bs_node, target_indices):
    return [cmds.sculptTarget(bs_node, e=True, regenerate=True, t=idx)[0]
            for idx in target_indices]


def __hide(rebuilt_targets):
    [cmds.hide(t) for t in rebuilt_targets]
