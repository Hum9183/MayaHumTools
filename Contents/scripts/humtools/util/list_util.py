# -*- coding: utf-8 -*-


def try_get_item(_list, index):
    """listへのgetitemを試みる。IndexErrorがraiseされた場合はFalseが返る

    Args:
        _list (list[any]): リスト
        index (int): getitemしたいインデックス

    Returns:
        element, success (any, bool): 要素、getitemが成功したかどうか
    """
    if _list is False:
        return None, False

    try:
        return _list[index], True
    except IndexError:
        return None, False
