# -*- coding: utf-8 -*-
from maya import cmds, mel

from .const import Const
from .blendshapedvertexmerger import setup as bsvm_setup


def execute():
    mel.eval('''
    buildViewMenu MayaWindow|mainWindowMenu;
    setParent -menu "MayaWindow|mainWindowMenu";
    ''')
    __add_menu()


def __add_folder():
    cmds.menuItem(divider=True)
    cmds.menuItem(
        Const.HUM_TOOLS_FOLDER,
        label=Const.HUM_TOOLS,
        subMenu=True,
        tearOff=True)


def __add_menu():
    __add_folder()
    bsvm_setup.setup()
