# -*- coding: utf-8 -*-

from maya import cmds

from .lang_op_var import LangOpVar
from ..util.extensions import Extensions
from ..util.lang import Lang
from ..util.log import Log
from ..util.progress_window import ProgressWindow


class DeformerWeightsExporter:
    def __init__(self, xmls_folder_path, xml_text_scroll_list):
        self.__xmls_folder_path = xmls_folder_path
        self.__xml_text_scroll_list = xml_text_scroll_list

    def export_xmls(self, mesh_parent_transform_and_skincluster_dict):
        progress_window = ProgressWindow(len(mesh_parent_transform_and_skincluster_dict),
                                         Lang.pack(u'XMLを生成中...', 'Creating XMLs...', LangOpVar.get()),
                                         LangOpVar.get())
        progress_window.show()

        for mesh_parent_transform, skin_cluster in mesh_parent_transform_and_skincluster_dict.items():
            # ProgressWindowの更新処理
            if progress_window.is_cancelled():
                break
            progress_window.next()

            xml_file_name = self.__get_xml_file_name(mesh_parent_transform)
            self.__export_xmls(xml_file_name, skin_cluster)
            self.__log(mesh_parent_transform)

        progress_window.close()
        self.__load_text_scroll_list()

    def __get_xml_file_name(self, mesh_parent_transform):
        return '{}{}'.format(mesh_parent_transform, Extensions.XML)

    def __export_xmls(self, xml_file_name, skin_cluster):
        cmds.deformerWeights(
            xml_file_name,
            export=True,
            deformer=skin_cluster,
            path=self.__xmls_folder_path)

    def __log(self, mesh_parent_transform):
        log_msg = Lang.pack(u'{}のXMLを作成しました。'.format(mesh_parent_transform),
                            'XML of {} was created.'.format(mesh_parent_transform),
                            LangOpVar.get())
        Log.log(log_msg)

    def __load_text_scroll_list(self):
        self.__xml_text_scroll_list.load()
