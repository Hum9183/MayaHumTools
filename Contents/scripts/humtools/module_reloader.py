# -*- coding: utf-8 -*-
from .hum_tools_const import HumToolsConst


def reload_a_few_times(modules):
    [__reload(modules) for _ in range(2)] # NOTE: 一回のreloadではリロードしきれない？


def __reload(modules):
    [__reload_py_ver(m) for m in modules]


def __reload_py_ver(module):
    if HumToolsConst.is_python_major_version_2():
        reload(module)      # Python2   Global空間の組み込みreload
    else:
        import importlib    # Python3
        importlib.reload(module)
