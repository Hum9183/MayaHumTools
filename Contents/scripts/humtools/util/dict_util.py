# -*- coding: utf-8 -*-


def delete_elements_with_the_value_none(_dict):
    """辞書の要素のうち、valueがNoneのものを削除する。

    Args:
        _dict (dict): 辞書

    Returns:
        dict: valueがNoneの要素を削除した辞書。
    """
    is_dict = type(_dict) is dict
    if is_dict:
        return {k: v for k, v in _dict.items() if v is not None}
    else:
        return None