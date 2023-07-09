# -*- coding: utf-8 -*-
from maya import cmds, mel
import maya.api.OpenMaya as om2


# ツール
def select_tool():
    """選択ツール"""
    mel.eval('SelectToolOptionsMarkingMenu')
    mel.eval('SelectToolOptionsMarkingMenuPopDown')

def art_paint_skin_weights_tool():
    mel.eval('ArtPaintSkinWeightsToolOptions')


# モード
def object_mode(mesh):
    mel.eval('maintainActiveChangeSelectMode {} 1'.format(mesh))

def vert_mode(mesh):
    build_model_panel4_object_pop()
    mel.eval('doMenuComponentSelectionExt("{}", "vertex", 1)'.format(mesh))

def build_model_panel4_object_pop():
    # mayaを起動して一度もビューポートでRMBをしてない場合は、ビルドする必要がある
    mel.eval('buildObjectMenuItemsNow "MainPane|viewPanes|modelPanel4|modelPanel4|modelPanel4|modelPanel4ObjectPop"')


# NOTE: 処理の備忘録
# def reset_selection_mode():
#     """無選択状態にする"""
#     om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
#     om2.MGlobal.setActiveSelectionList(om2.MSelectionList())
