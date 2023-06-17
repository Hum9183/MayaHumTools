# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

from maya import cmds, mel

from ..util.extensions import Extensions
from ..util.lang       import Lang
from ..util.log        import Log
from ..util.node_type  import NodeType
from ..util            import path
from .lang_op_var      import LangOpVar


class AutoSkinBinder:
    def __init__(self, xmls_folder_path, mesh_parent_transform_and_skincluster_dict):
        self.__xmls_folder_path    = xmls_folder_path
        self.__mesh_parent_transform_and_skincluster_dict = mesh_parent_transform_and_skincluster_dict

    def bind(self):
        [self.__bind(mesh_parent_transform, skin_cluster)
            for mesh_parent_transform, skin_cluster in self.__mesh_parent_transform_and_skincluster_dict.items()]

    def get_dict_skin_bound(self):
        return {mesh_parent_transform: NodeType.get_history(mesh_parent_transform, NodeType.SKIN_CLUSTER)
                for mesh_parent_transform in self.__mesh_parent_transform_and_skincluster_dict.keys()}

    def __bind(self, mesh_parent_transform, skin_cluster):
        if skin_cluster is not None:
            return
        joints = self.__get_joints_from_xml(mesh_parent_transform)
        if joints is None:
            return
        self.__smooth_bind_skin(mesh_parent_transform, joints)

    def __get_joints_from_xml(self, mesh_parent_transform):
        xml_file_name = '{}{}'.format(mesh_parent_transform, Extensions.XML)
        xml_path = path.combine([self.__xmls_folder_path, xml_file_name])
        try:
            element_tree = ET.parse(xml_path)
        except IOError:
            warning_msg = Lang.pack(u'{}と同名のXMLが存在しないため、自動バインドができませんでした。'.format(mesh_parent_transform),
                                    'Auto binding could not be performed because XML with the same name as {} does not exist.'.format(mesh_parent_transform),
                                    LangOpVar.get())
            Log.warning(warning_msg)
            return None
        root = element_tree.getroot()
        joints = [weights.attrib['source'] for weights in root.iter('weights')]
        return joints

    def __smooth_bind_skin(self, mesh_parent_transform, joints):
        cmds.select(mesh_parent_transform, replace=True)
        cmds.select(joints, add=True)
        mel.eval('SmoothBindSkin') # NOTE: userの既存オプション設定準拠でバインドする
        cmds.select(cl=True)
        self.__remove_unnecessary_influences(mesh_parent_transform, joints)
        log_msg = Lang.pack(u'{}にジョイントをバインドしました。'.format(mesh_parent_transform),
                            'Joints bound to {}.'.format(mesh_parent_transform),
                            LangOpVar.get())
        Log.log(log_msg)

    def __remove_unnecessary_influences(self, mesh_parent_transform, joints):
        # NOTE: SmoothBindSkinによるバインドだと骨が全てインフルエンスに入ってしまうため、余分なインフルエンスを削除する
        skin_cluster = NodeType.get_history(mesh_parent_transform, NodeType.SKIN_CLUSTER)
        influences = cmds.skinCluster(skin_cluster, q=True, influence=True)
        unnecessary_influences = list(set(influences) - set(joints))
        for infl in unnecessary_influences:
            cmds.skinCluster(skin_cluster, e=True, removeInfluence=infl)
