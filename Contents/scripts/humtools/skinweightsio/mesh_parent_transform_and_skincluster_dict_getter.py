# -*- coding: utf-8 -*-

from maya import cmds

from ..util.lang             import Lang
from ..util.log              import Log
from ..util.node_type        import NodeType
from ..util.unexpected_error import UnexpectedError
from ..util                  import dict_util
from .lang_op_var            import LangOpVar




def get_for_export(mesh_parent_transforms):
    transform_and_skincluster_dict = __get(mesh_parent_transforms)
    __exists_skincluster_log(transform_and_skincluster_dict)
    normalized_dict = dict_util.delete_elements_with_the_value_none(transform_and_skincluster_dict)
    err_msg = Lang.pack(u'skinClusterを持つメッシュを選択してください。', 'Select the meshes that has skinCluster.', LangOpVar.get())
    __exist_validation(normalized_dict, err_msg)
    return normalized_dict


def get_for_import(mesh_parent_transforms):
    transform_and_skincluster_dict = __get(mesh_parent_transforms)
    err_msg = Lang.pack(u'メッシュを選択してください。', 'Please select the meshes.', LangOpVar.get())
    __exist_validation(transform_and_skincluster_dict, err_msg)
    return transform_and_skincluster_dict


def __exists_skincluster_log(transform_and_skincluster_dict):
    for transform, skin_cluster in transform_and_skincluster_dict.items():
        if skin_cluster is None:
            err_msg = Lang.pack(u'{}にskinClusterが存在しないため、XMLを作成できませんでした。'.format(transform),
                                'XML could not be created because skinCluster does not exist in {}'.format(transform),
                                LangOpVar.get())
            Log.warning(err_msg)


def __exist_validation(_dict, err_text):
    if _dict == {}:
        raise UnexpectedError(err_text)


def __get(mesh_parent_transforms):
    """メッシュの親トランスフォームとSkinClusterの辞書を取得する"""
    return {t: NodeType.get_history(t, NodeType.SKIN_CLUSTER)
            for t in mesh_parent_transforms}
