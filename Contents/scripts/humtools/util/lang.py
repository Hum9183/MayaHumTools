# -*- coding: utf-8 -*-
from ..hum_tools_const import HumToolsConst


class Lang:
    ja_JP = 'ja_JP'
    en_US = 'en_US'

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