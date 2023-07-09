# -*- coding: utf-8 -*-
from maya import cmds, mel

from .hum_tools_const import HumToolsConst
from .blendshapedvertexmerger import setup as bsvm_setup
from .blendshapedmesheditor   import setup as bsme_setup
from .skinweightsbugsearcher  import setup as swbs_setup
from .skinweightsio           import setup as swio_setup


def execute():
    mel.eval('''
    buildViewMenu MayaWindow|mainWindowMenu;
    setParent -menu "MayaWindow|mainWindowMenu";
    ''')
    __add_menu()


def __add_folder():
    cmds.menuItem(divider=True)
    cmds.menuItem(
        HumToolsConst.HUM_TOOLS_FOLDER,
        label=HumToolsConst.HUM_TOOLS,
        subMenu=True,
        tearOff=True)


def __add_menu():
    __add_folder()
    bsvm_setup.add_menu()
    bsme_setup.add_menu()
    swio_setup.add_menu()
    swbs_setup.add_menu()
