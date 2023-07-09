# -*- coding: utf-8 -*-
from maya import cmds, mel

from ..lib                   import tool_mode
from ..util.lang             import Lang
from ..util.unexpected_error import UnexpectedError
from .lang_op_var            import LangOpVar


class WeightsBugTextScrollList:
    def __init__(self, name):
        self.__name = name

    def build(self):
        cmds.paneLayout(configuration='horizontal2') # NOTE: singleだとうまくadjustしない
        ann_text_ja = u'クリックするとバグ頂点が選択されます。\nダブルクリックするとバグウェイトが振られているジョイントを選択します。'
        ann_text_en = 'Clicking selects the bug vertex. \nDouble-clicking selects the joint to which the bug weight is assigned.'
        cmds.textScrollList(self.__name,
                            ann=Lang.pack(ann_text_ja, ann_text_en, LangOpVar.get()),
                            allowMultiSelection=False,
                            selectCommand     =lambda *args: self.__select_vert(),
                            doubleClickCommand=lambda *args: self.__select_joint())

    def delete_sel_item(self):
        sel_item = self.__get_sel_item()
        cmds.textScrollList(self.__name, e=True, removeItem=sel_item)

    def set_new_items(self, items):
        self.delete_all_items()
        self.__add_items(items)

    def delete_all_items(self):
        cmds.textScrollList(self.__name, e=True, removeAll=True)

    def __add_items(self, items):
        cmds.textScrollList(self.__name, e=True, append=items)

    @UnexpectedError.catch
    def __select_vert(self):
        mesh, mesh_vert, joint = self.__get_bug_items(validate_exists=True)

        tool_mode.select_tool() # NOTE: ArtPaintSkinWeightsTool等になっている場合、選択ツールに戻すために呼ぶ
        cmds.select(cl=True)

        tool_mode.vert_mode(mesh)
        cmds.select(mesh_vert, r=True)

        tool_mode.art_paint_skin_weights_tool()
        mel.eval('setSmoothSkinInfluence {}'.format(joint)) # インフルエンスの選択

    @UnexpectedError.catch
    def __select_joint(self):
        _, _, joint = self.__get_bug_items(validate_exists=True)
        cmds.select(joint, r=True)

    @UnexpectedError.catch
    def __get_sel_item(self):
        sel_item = cmds.textScrollList(self.__name, q=True, selectItem=True)
        if sel_item:
            return sel_item[0]
        else:
            raise UnexpectedError(Lang.pack(u'バグ項目が存在しません。', 'Bug item does not exist.', LangOpVar.get()))

    def __get_bug_items(self, validate_exists=False):
        sel_item = self.__get_sel_item()
        at_split    = sel_item.split('@')
        mesh_vert   = at_split[0]
        first_joint = at_split[1] # NOTE: ２つ目以降のジョイントがある場合でも無視する
        mesh        = mesh_vert.split('.')[0]

        if validate_exists:
            self.__exists_validation(mesh, first_joint)

        return mesh, mesh_vert, first_joint

    def __exists_validation(self, mesh, joint):
        # NOTE: 頂点番号はなかったとしても無視する(選択はできてしまう)
        if cmds.objExists(mesh) is False:
            non_existent = mesh
        elif cmds.objExists(joint) is False:
            non_existent = joint
        else:
            return

        ja = u'{}がシーン内に存在しません。'.format(non_existent)
        en = u'{} does not exist in the scene.'.format(non_existent)
        raise UnexpectedError(Lang.pack(ja, en, LangOpVar.get()))
