# -*- coding: utf-8 -*-
from itertools import chain

from maya import cmds

from ..util.node_type import NodeType
from ..util.unexpected_error import UnexpectedError


def get_nodes(mesh, raise_ex_if_is_none=False):
    """BSノードを取得する

    Args:
        mesh (str): メッシュ

    Returns:
        list[str] or None: BSノードのリスト
    """
    return NodeType.get_histories(mesh, NodeType.BLEND_SHAPE, raise_ex_if_is_none)


def exists_validate(bs_nodes):
    """ブレンドシェイプが存在するかを確認する

    Args:
        bs_nodes (list[str]): BSノードのリスト

    Raises:
        UnexpectedError: listが空の場合
    """
    if bs_nodes == []:
        raise UnexpectedError(u'ブレンドシェイプが存在しません。')


def get_target_indices(bs_node):
    """BSターゲットのインデックスを取得する。
    ShapeEditorの並び順と同一。

    Args:
        bs_node (str): BSノード

    Returns:
        list[long]: BSターゲットのインデックスのリスト
    """
    return cmds.getAttr('{}.targetDirectory[0].childIndices'.format(bs_node))


def get_rebuilt_target_meshes(bs_node):
    """リビルド済のターゲットメッシュのリストを取得する。
    ShapeEditorの並び順ではなく、index順。

    Args:
        bs_node (str): BSノード

    Returns:
        list[str]: リビルド済のターゲットメッシュのリスト
    """
    return cmds.blendShape(bs_node, q=True, t=True)


def delete_rebuilt_target_meshes(bs_nodes):
    """リビルド済のターゲットメッシュを削除する。

    Args:
        bs_node (list[str] or str): BSノード
    """
    def delete(bs_node):
        rebuilt_target_meshes = get_rebuilt_target_meshes(bs_node)
        if (rebuilt_target_meshes != []):
            cmds.delete(rebuilt_target_meshes)

    if type(bs_nodes) is list:
        [delete(bs) for bs in bs_nodes]
    else:
        delete(bs_nodes)


def sort_targets_by_shape_editor_display_order(target_indices, target_meshes):
    """リビルド済のメッシュListをShapeEditorの並び順にソートする"""
    return [m for _, m in sorted(zip(target_indices, target_meshes))]


def get_targets_tuples(bs_node):
    """ターゲットのindexとリビルド済メッシュ名がペアになったタプルのリストを取得する。
    ターゲットがすべてリビルド済であることを想定。
    ShapeEditorの並び順にソートする。

    Args:
        bs_node (str): BSノード

    Returns:
        list[(long, string)]: (ターゲットのindex, リビルド済メッシュ名)のリスト
    """
    target_indices = get_target_indices(bs_node)
    target_meshes = get_rebuilt_target_meshes(bs_node)
    sorted_target_meshes = sort_targets_by_shape_editor_display_order(
        target_indices, target_meshes)
    return zip(target_indices, sorted_target_meshes)
