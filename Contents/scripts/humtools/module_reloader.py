# -*- coding: utf-8 -*-

def reload_py_ver(modules):
    [__reload_py_ver(m) for m in modules]


def __reload_py_ver(module):
    # TODO: どこかでバージョン取得して、そこを参照するようにする
    try:
        reload(module)      # Python2   Global空間の組み込みreload
    except NameError:
        import importlib    # Python3
        importlib.reload(module)
