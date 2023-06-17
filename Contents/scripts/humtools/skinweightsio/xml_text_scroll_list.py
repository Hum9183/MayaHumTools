# -*- coding: utf-8 -*-
import os

from maya import cmds

from ..util.extensions       import Extensions
from ..util.lang             import Lang
from ..util.unexpected_error import UnexpectedError
from ..util                  import path
from .lang_op_var            import LangOpVar


class XMLTextScrollList:
    def __init__(self, name, xmls_folder_path):
        self.__name = name
        self.__xmls_folder_path = xmls_folder_path

    def build(self):
        cmds.paneLayout(configuration='horizontal2') # NOTE: singleだとうまくadjustしない
        cmds.textScrollList(self.__name,
                            allowMultiSelection=True,
                            deleteKeyCommand=lambda *args: self.delete_xml_files_and_items())

    def load(self):
        files = os.listdir(self.__xmls_folder_path)
        xmls = [f for f in files if f.endswith(Extensions.XML)]
        cmds.textScrollList(self.__name, e=True, removeAll=True)
        cmds.textScrollList(self.__name, e=True, append=xmls)

    @UnexpectedError.catch
    def delete_xml_files_and_items(self, all=False):
        selItems = self.__get_selected_items(all)
        self.__delete_xml_files(selItems)
        self.load()

    def __get_selected_items(self, all=False):
        if all:
            selItems = cmds.textScrollList(self.__name, q=True, allItems=True)
            if selItems is None:
                raise UnexpectedError(Lang.pack(u'XMLが存在しません。', 'XML does not exist.', LangOpVar.get()))
        else:
            selItems = cmds.textScrollList(self.__name, q=True, selectItem=True)
            if selItems is None:
                raise UnexpectedError(Lang.pack(u'削除したいXMLを選択してください。', 'Select the XML you wish to delete.', LangOpVar.get()))
        return selItems

    def __delete_xml_files(self, selItems):
        xml_file_paths = [path.combine([self.__xmls_folder_path, item]) for item in selItems]
        [os.remove(f) for f in xml_file_paths]

