# -*- coding: utf-8 -*-
from maya import cmds

from ..hum_tools_const import HumToolsConst
from .const import Const


class LangOpVar:
    op_var_name = '{}{}'.format(Const.TOOL_NAME, HumToolsConst.LANG)

    @staticmethod
    def get():
        if cmds.optionVar(exists=LangOpVar.op_var_name) is False:
            LangOpVar.set(HumToolsConst.LANGUAGE)
        return cmds.optionVar(q=LangOpVar.op_var_name)

    @staticmethod
    def set(lang):
        cmds.optionVar(stringValue=(LangOpVar.op_var_name, lang))