# -*- coding: utf-8 -*-
import subprocess
import webbrowser

from maya import cmds
from maya.common.ui import LayoutManager

from ..util.extensions       import Extensions
from ..util.hum_window_base  import HumWindowBase
from ..util.lang             import Lang
from ..util                  import path
from .const                  import Const
from .lang_op_var            import LangOpVar
from .option_settings        import OptionSettings
from .xml_text_scroll_list   import XMLTextScrollList
from .                       import main


class Window(HumWindowBase):
    def __init__(self, tool_name):
        super(Window, self).__init__(tool_name)

        self.__xmls_folder_path            = ''
        self.__option_settings_folder_path = ''

        self.__option_settings      = None
        self.__xml_text_scroll_list = None

    def _create_window(self):
        cmds.window(self.tool_name, title=self.tool_name, menuBar=True, mxb=False, mnb=False)
        self.__set_paths()
        self.__create_this_app_data_folders()
        self.__setup_option_settings()
        self.__set_xml_text_scroll_list()
        self.__build_guis()

    def __set_paths(self):
        humtools_app_data_folder = path.get_humtools_app_data_folder_path()
        this_app_data_folder_path = path.combine([humtools_app_data_folder, self.tool_name])
        self.__xmls_folder_path            = path.combine([this_app_data_folder_path, Const.XMLS_FOLDER_NAME])
        self.__option_settings_folder_path = path.combine([this_app_data_folder_path, Const.OPTION_SETTINGS_FOLDER_NAME])

    def __create_this_app_data_folders(self):
        path.create_folder_recursive(self.__xmls_folder_path)
        path.create_folder_recursive(self.__option_settings_folder_path)

    def __setup_option_settings(self):
        json_name = '{}{}'.format(Const.OPTION_SETTINGS_JSON_NAME, Extensions.JSON)
        json_path = path.combine([self.__option_settings_folder_path, json_name])
        self.__option_settings = OptionSettings(json_path)
        self.__option_settings.create()
        self.__option_settings.load()

    def __set_xml_text_scroll_list(self):
        self.__xml_text_scroll_list = XMLTextScrollList(Const.XML_TEXT_SCROLL_LIST_NAME, self.__xmls_folder_path)

    def __build_guis(self):
        lang = LangOpVar.get()
        self.__build_edit_menus(lang)
        self.__build_option_menus(lang)
        self.__build_help_menus(lang)
        self.__build_run_buttons(lang)
        self.__xml_text_scroll_list.build()
        self.__xml_text_scroll_list.load()

    def __build_edit_menus(self, lang):
        cmds.menu(l=Lang.pack(u'編集', 'Edit', lang), tearOff=True)
        cmds.menuItem(l=Lang.pack(u'XMLを削除', 'Delete XML', lang), c=lambda *args: self.__xml_text_scroll_list.delete_xml_files_and_items())
        cmds.menuItem(l=Lang.pack(u'XMLをすべて削除', 'Delete all XML', lang), c=lambda *args: self.__xml_text_scroll_list.delete_xml_files_and_items(all=True))

    def __build_option_menus(self, lang):
        cmds.menu(l=Lang.pack(u'オプション', 'Option', lang), tearOff=True)
        self.__build_import_mothod_radio_menu(lang)
        self.__menu_divider()
        labels = [Lang.pack(u'名前を無視', 'Ignore name', lang),
                  Lang.pack(u'ウェイトを正規化', 'Normalize weights', lang),
                  Lang.pack(u'自動バインド', 'Auto binding', lang)]
        cmds.menuItem(l=labels[0], checkBox=self.__option_settings.ignore_name,       c=lambda *args: self.__option_settings.toggle_ignore_name())
        cmds.menuItem(l=labels[1], checkBox=self.__option_settings.normalize_weights, c=lambda *args: self.__option_settings.toggle_normalize_weights())
        self.__menu_divider()
        cmds.menuItem(l=labels[2], checkBox=self.__option_settings.auto_binding,      c=lambda *args: self.__option_settings.toggle_auto_binding())

    def __build_import_mothod_radio_menu(self, lang):
        cmds.menuItem(l=Lang.pack(u'マッピング方法', 'Import method', lang), subMenu=True, tearOff=True)
        cmds.radioMenuItemCollection()
        labels = [Lang.pack(u'インデックス', 'Index', lang), Lang.pack(u'オーバー', 'Over', lang), Lang.pack(u'二アレスト', 'Nearest', lang)]
        current_import_method = self.__option_settings.import_method
        cmds.menuItem(l=labels[0], radioButton=(current_import_method == Const.METHOD_INDEX),   c=lambda *args: self.__option_settings.set_import_method(Const.METHOD_INDEX))
        cmds.menuItem(l=labels[1], radioButton=(current_import_method == Const.METHOD_OVER),    c=lambda *args: self.__option_settings.set_import_method(Const.METHOD_OVER))
        cmds.menuItem(l=labels[2], radioButton=(current_import_method == Const.METHOD_NEAREST), c=lambda *args: self.__option_settings.set_import_method(Const.METHOD_NEAREST))
        cmds.setParent('..', menu=True)

    def __build_help_menus(self, lang):
        cmds.menu(l=Lang.pack(u'ヘルプ', 'Help', lang), tearOff=True, helpMenu=True)
        cmds.menuItem(l=Lang.pack(u'ドキュメントを開く', 'Open document', lang), c=lambda *args: self.__open_document_in_webbrowser())
        self.__menu_divider()
        cmds.menuItem(l=Lang.pack(u'オプション設定のリセット', 'Reset option settings', lang), c=lambda *args: self.__reset_option_settings())
        self.__menu_divider()
        self.__build_language_radio_menu(lang)
        self.__menu_divider()
        cmds.menuItem(l=Lang.pack(u'XMLフォルダを開く', 'Open XML Folder', lang), c=lambda *args: self.__open_xmls_folder_in_explorer())

    def __build_language_radio_menu(self, lang):
        cmds.menuItem(l=Lang.select(['Language', '言語', '语言'], lang), subMenu=True, tearOff=True)
        cmds.radioMenuItemCollection()
        labels = ['English', '日本語', '简体中文']
        cmds.menuItem(l=labels[0], radioButton=(lang == Lang.en_US), c=lambda *args: self.__set_lang_option_var(Lang.en_US))
        cmds.menuItem(l=labels[1], radioButton=(lang == Lang.ja_JP), c=lambda *args: self.__set_lang_option_var(Lang.ja_JP))
        cmds.menuItem(l=labels[2], radioButton=(lang == Lang.zh_CN), c=lambda *args: self.__set_lang_option_var(Lang.zh_CN))
        cmds.setParent('..', menu=True)

    def __set_lang_option_var(self, lang):
        LangOpVar.set(lang)
        super(Window, self).reload_window()

    def __open_document_in_webbrowser(self):
        url = 'https://github.com/Hum9183/MayaHumTools#skinweightsio'
        webbrowser.open(url)

    def __open_xmls_folder_in_explorer(self):
        subprocess.Popen(['explorer', self.__xmls_folder_path], shell=True)

    def __reset_option_settings(self):
        self.__option_settings.reset()
        super(Window, self).reload_window() # NOTE: GUIを更新するためにウィンドウをリロードする

    def __build_run_buttons(self, lang):
        with LayoutManager(cmds.rowLayout(nc=3)):
            cmds.button(l=Lang.pack(u'XMLの作成', 'Create XMLs', lang),
                        ann=Lang.pack(u'メッシュを選択してボタンを押すとXMLファイルが生成されます。',
                                      'Select the meshes and press this button to create XML files.',
                                      lang),
                        w=128,
                        c=lambda *args: self.__create_xml_wrapper())
            cmds.text(l='', w=1)
            cmds.button(l=Lang.pack(u'ウェイトのコピー', 'Copy weights', lang),
                        ann=Lang.pack(u'メッシュを選択してボタンを押すと、メッシュと同名のXMLを自動で探し出し、スキンウェイトをコピーします。',
                                      'Select the meshes and press this button to automatically find the XML with the same name as the meshes and copy the skin weights.',
                                      lang),
                        w=128,
                        c=lambda *args: self.__copy_weights_wrapper())

    def __create_xml_wrapper(self):
        main.create_xml(self.__xmls_folder_path, self.__xml_text_scroll_list)

    def __copy_weights_wrapper(self):
        main.copy_weights(self.__xmls_folder_path, self.__option_settings)

    def __menu_divider(self):
        cmds.menuItem(divider=True)
