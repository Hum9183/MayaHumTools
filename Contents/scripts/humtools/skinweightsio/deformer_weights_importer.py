# -*- coding: utf-8 -*-
import os

from maya import cmds

from ..util.extensions import Extensions
from ..util.lang       import Lang
from ..util.log        import Log
from ..util            import path
from .lang_op_var      import LangOpVar


class DeformerWeightsImporter:
    def __init__(self, xmls_folder_path, option_settings):
        self.__xmls_folder_path  = xmls_folder_path
        self.__option_settings = option_settings

    def import_xmls(self, transform_and_skincluster_dict):
        xmls_folder_path  = self.__xmls_folder_path
        import_method     = self.__option_settings.import_method
        ignore_name       = self.__option_settings.ignore_name
        normalize_weights = self.__option_settings.normalize_weights

        # NOTE: xmlと同名のメッシュ(メッシュの親トランスフォーム)に自動でウェイトをコピーする
        for mesh_parent_transform, skin_cluster in transform_and_skincluster_dict.items():
            xml_file_name = self.__get_xml_file_name(mesh_parent_transform)
            if self.__exists_xml_file(xmls_folder_path, xml_file_name, mesh_parent_transform) is False:
                continue

            cmds.deformerWeights(
                                xml_file_name,
                                im=True,
                                method=import_method,
                                ignoreName=ignore_name,
                                deformer=skin_cluster,
                                path=xmls_folder_path)
            self.__normalize_weights(skin_cluster, normalize_weights)
            log_msg = Lang.pack(u'{}にウェイトをコピーしました。'.format(mesh_parent_transform),
                                'Copied weights to {}.'.format(mesh_parent_transform),
                                LangOpVar.get())
            Log.log(log_msg)
        # self.__option_settings.log()

    def __get_xml_file_name(self, mesh_parent_transform):
        return '{}{}'.format(mesh_parent_transform, Extensions.XML)

    def __exists_xml_file(self, xmls_folder_path, xml_file_name, mesh_parent_transform):
        xml_file_path = path.combine([xmls_folder_path, xml_file_name])
        if os.path.isfile(xml_file_path):
            return True
        else:
            warning_msg = Lang.pack(u'{}と同名のXMLが存在しないため、ウェイトコピーができませんでした。'.format(mesh_parent_transform),
                                    'Weight copy could not be performed because XML with the same name as {} does not exist.'.format(mesh_parent_transform),
                                    LangOpVar.get())
            Log.warning(warning_msg)
            return False

    def __normalize_weights(self, skin_cluster, normalize_weights):
        if normalize_weights:
            cmds.skinCluster(skin_cluster, e=True, forceNormalizeWeights=True)
