# -*- coding: utf-8 -*-
import webbrowser

from maya import cmds, mel
from maya.common.ui import LayoutManager

from ..lib                         import tool_mode
from ..util.hum_window_base        import HumWindowBase
from ..util.lang                   import Lang
from ..util.unexpected_error       import UnexpectedError
from ..util                        import in_view_message
from .const                        import Const
from .lang_op_var                  import LangOpVar
from .weights_bug_text_scroll_list import WeightsBugTextScrollList
from .                             import bug_searcher


class Window(HumWindowBase):
    def __init__(self, tool_name):
        super(Window, self).__init__(tool_name)
        self.__weights_bug_text_scroll_list = None

    def _create_window(self):
        cmds.window(self.tool_name, title=self.tool_name, menuBar=True, mxb=False, mnb=False)
        self.__set_text_scroll_list()
        self.__build_guis()

    def __set_text_scroll_list(self):
        self.__weights_bug_text_scroll_list = WeightsBugTextScrollList(Const.WEIGHTS_BUG_TEXT_SCROLL_LIST_NAME)

    def __build_guis(self):
        lang = LangOpVar.get()
        self.__build_edit_menus(lang)
        self.__build_help_menus(lang)
        self.__build_button(lang)
        self.__weights_bug_text_scroll_list.build()

    def __build_edit_menus(self, lang):
        cmds.menu(l=Lang.pack(u'編集', 'Edit', lang), tearOff=True)
        cmds.menuItem(l=Lang.pack(u'選択しているバグ項目を削除', 'Delete selected bug item', lang), c=lambda *args: self.__weights_bug_text_scroll_list.delete_sel_item())

    def __build_help_menus(self, lang):
        cmds.menu(l=Lang.pack(u'ヘルプ', 'Help', lang), tearOff=True, helpMenu=True)
        cmds.menuItem(l=Lang.pack(u'ドキュメントを開く', 'Open document', lang), c=lambda *args: self.__open_document_in_webbrowser())
        self.__menu_divider()
        self.__build_language_radio_menu(lang)

    def __build_language_radio_menu(self, lang):
        cmds.menuItem(l=Lang.pack(u'言語', 'Language', lang), subMenu=True, tearOff=True)
        cmds.radioMenuItemCollection()
        labels = [Lang.pack(u'日本語', 'Japanese', lang), Lang.pack(u'英語', 'English', lang)]
        cmds.menuItem(l=labels[0], radioButton=(lang == Lang.ja_JP), c=lambda *args: self.__set_lang_option_var(Lang.ja_JP))
        cmds.menuItem(l=labels[1], radioButton=(lang == Lang.en_US), c=lambda *args: self.__set_lang_option_var(Lang.en_US))
        cmds.setParent('..', menu=True)

    def __set_lang_option_var(self, lang):
        LangOpVar.set(lang)
        super(Window, self).reload_window()

    def __open_document_in_webbrowser(self):
        url = 'https://github.com/Hum9183/MayaHumTools'
        webbrowser.open(url)

    def __build_button(self, lang):
        with LayoutManager(cmds.columnLayout(adj=True)):
            ann_text_ja = u'メッシュを選択してボタンを押すとウェイトバグのスキャンをスタートします。\nスキャンが終了すると、テキストリストにバグがリストアップされます。'
            ann_text_en = 'Select meshes and press this button to start scanning for weight bugs.\nWhen the scan is complete, the bug will be listed in the text list.'
            cmds.button(l=Lang.pack(u'ウェイトバグを探す', 'Search weights bug', lang),
                        ann=Lang.pack(ann_text_ja, ann_text_en, lang),
                        c=lambda *args: self.__main())

    @UnexpectedError.catch
    def __main(self):
        # NOTE: skinweightペイントモードだった場合処理が重くなるため、あらかじめ選択ツールにする
        tool_mode.select_tool()

        bugs = bug_searcher.search()
        bug_count = len(bugs)

        if bug_count == 0:
            self.__weights_bug_text_scroll_list.delete_all_items()
            completion_text = Lang.pack(u"バグはありません。", 'No bugs.', LangOpVar.get())
        else:
            self.__weights_bug_text_scroll_list.set_new_items(bugs)
            completion_text = Lang.pack(u"{}個のバグが見つかりました。".format(bug_count), '{} bugs found.'.format(bug_count), LangOpVar.get())

        in_view_message.show(completion_text)

    def __menu_divider(self):
        cmds.menuItem(divider=True)
