# -*- coding: utf-8 -*-
import os

from maya import cmds

from .lang_op_var import LangOpVar
from ..util import path
from ..util.extensions import Extensions
from ..util.lang import Lang
from ..util.log import Log
from ..util.progress_window import ProgressWindow


class DeformerWeightsImporter:
    def __init__(self, xmls_folder_path, option_settings):
        self.__xmls_folder_path = xmls_folder_path
        self.__option_settings = option_settings

    def import_xmls(self, transform_and_skincluster_dict):
        xmls_folder_path = self.__xmls_folder_path
        import_method = self.__option_settings.import_method
        ignore_name = self.__option_settings.ignore_name
        normalize_weights = self.__option_settings.normalize_weights

        progress_window = ProgressWindow(len(transform_and_skincluster_dict),
                                         Lang.pack(u'ウェイトをコピー中...', 'Copying weights...', LangOpVar.get()),
                                         LangOpVar.get())
        progress_window.show()

        success = False
        # NOTE: xmlと同名のメッシュ(メッシュの親トランスフォーム)に自動でウェイトをコピーする
        for mesh_parent_transform, skin_cluster in transform_and_skincluster_dict.items():
            # ProgressWindowの更新処理
            if progress_window.is_cancelled():
                break
            if progress_window.is_greater_than_max():
                break
            progress_window.next()

            # XMLがあるか確認
            xml_file_name = self.__get_xml_file_name(mesh_parent_transform)
            if self.__exists_xml_file(xmls_folder_path, xml_file_name, mesh_parent_transform) is False:
                continue

            # ウェイトコピー処理
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
        else:
            success = True  # TODO: Falseの場合はUndoチャンクで囲ってUndoまでする

        progress_window.close()

        return success

    def __get_xml_file_name(self, mesh_parent_transform):
        return '{}{}'.format(mesh_parent_transform, Extensions.XML)

    def __exists_xml_file(self, xmls_folder_path, xml_file_name, mesh_parent_transform):
        xml_file_path = path.combine([xmls_folder_path, xml_file_name])
        if os.path.isfile(xml_file_path):
            return True
        else:
            ja_JP = u'{}と同名のXMLが存在しないため、ウェイトコピーができませんでした。'.format(mesh_parent_transform)
            en_US = 'Weight copy could not be performed because XML with the same name as {} does not exist.'.format(
                mesh_parent_transform)
            warning_msg = Lang.pack(ja_JP, en_US, LangOpVar.get())
            Log.warning(warning_msg)  # TODO: Logだけだと気が付きにくいためinViewMessageも出す
            return False

    def __normalize_weights(self, skin_cluster, normalize_weights):
        if normalize_weights:
            cmds.skinCluster(skin_cluster, e=True, forceNormalizeWeights=True)
