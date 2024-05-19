# -*- coding: utf-8 -*-
from . import str_util
from .list_util import try_get_item
from ..hum_tools_const import HumToolsConst


class Lang:
    en_US = 'en_US'
    en_US_index = 0
    ja_JP = 'ja_JP'
    ja_JP_index = 1
    zh_CN = 'zh_CN'
    zh_CN_index = 2

    @staticmethod
    def select(texts, select=None):
        """日本語の文字列と英語の文字列をパックし、適切な言語の文字列を返す。

        Args:
            texts (list[str]): テキストたちのリスト
            select (str, optional): 返す言語を指定する。デフォルトはNone。

        Returns:
            str: Mayaを立ち上げた言語の文字列を返す。select引数で指定した場合は、指定した言語の文字列を返す。

        Note:
            Mayaを立ち上げた言語やselectで指定した言語が日本語や英語、中国語以外の場合は、英語になる。
        """
        if select is None:
            lang = HumToolsConst.LANGUAGE
        else:
            lang = select

        text = str_util.EMPTY
        success = False
        if lang == Lang.en_US:
            text, success = try_get_item(texts, Lang.en_US_index)
        elif lang == Lang.ja_JP:
            text, success = try_get_item(texts, Lang.ja_JP_index)
        elif lang == Lang.zh_CN:
            text, success = try_get_item(texts, Lang.zh_CN_index)
        else:
            text, success = try_get_item(texts, Lang.en_US_index)

        if success:
            return str_util.decode(text)
        else:
            return str_util.EMPTY

    # noinspection PyPep8Naming
    @staticmethod
    def pack(_ja_JP, _en_US, select=None):
        """日本語の文字列と英語の文字列をパックし、適切な言語の文字列を返す。

        Args:
            _ja_JP (str): 日本語の文字列。
            _en_US (str): 英語の文字列。
            select (str, optional): 返す言語を指定する。デフォルトはNone。

        Returns:
            str: Mayaを立ち上げた言語の文字列を返す。select引数で指定した場合は、指定した言語の文字列を返す。

        Note:
            Mayaを立ち上げた言語やselectで指定した言語が日本語や英語以外の場合は、英語になる。
        """
        if select is None:
            lang = HumToolsConst.LANGUAGE
        else:
            lang = select

        if lang == Lang.ja_JP:
            return _ja_JP
        elif lang == Lang.en_US:
            return _en_US
        else:
            return _en_US
