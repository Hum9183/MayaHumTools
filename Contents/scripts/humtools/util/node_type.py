# -*- coding: utf-8 -*-
from maya import cmds

from ..util.lang             import Lang
from ..util.readonly         import metaclass
from ..util.unexpected_error import UnexpectedError
from ..hum_tools_const       import HumToolsConst


class NodeType(metaclass('NodeType')):
    BLEND_SHAPE  = 'blendShape'
    MESH         = 'mesh'
    SKIN_CLUSTER = 'skinCluster'
    TWEAK        = 'tweak'

    @staticmethod
    def get_history(mesh, sort_type, raise_ex_if_is_none=False, lang=HumToolsConst.LANGUAGE):
        """メッシュから指定のヒストリを取得する。単体版。

        Args:
            mesh (str): メッシュ
            sort_type (str): 取得したいヒストリのタイプ。
            raise_ex_if_is_none (bool, optional): ヒストリがなかった場合に例外を出すかどうか。デフォルトはFalse。
            lang (str, optional): 例外に使用する文字列の言語。デフォルトはHumToolsConst.LANGUAGE。

        Returns:
            str: ヒストリ。ない場合はNoneを返す。
        """
        histories = NodeType.__get_histories(mesh, sort_type, raise_ex_if_is_none, lang)
        if histories == []:
            return None
        return histories[0]

    @staticmethod
    def get_histories(mesh, sort_type, raise_ex_if_is_none=False, lang=HumToolsConst.LANGUAGE):
        """メッシュから指定のヒストリを取得する。複数版。

        Args:
            mesh (str): メッシュ
            sort_type (str): 取得したいヒストリのタイプ。
            raise_ex_if_is_none (bool, optional): ヒストリがなかった場合に例外を出すかどうか。デフォルトはFalse。
            lang (str, optional): 例外に使用する文字列の言語。デフォルトはHumToolsConst.LANGUAGE。

        Returns:
            list[str]: ヒストリ
        """
        return NodeType.__get_histories(mesh, sort_type, raise_ex_if_is_none, lang)

    @staticmethod
    def __get_histories(mesh, sort_type, raise_ex_if_is_none, lang):
        """メッシュから指定のヒストリを取得する。本処理。

        Args:
            mesh (str): メッシュ
            sort_type (str): 取得したいヒストリのタイプ。
            raise_ex_if_is_none (bool): ヒストリがなかった場合に例外を出すかどうか。
            lang (str): 例外に使用する文字列の言語。

        Raises:
            UnexpectedError: ヒストリが無く、かつraise_ex_if_is_noneがTrueの場合に投げる。

        Returns:
            list[str]: ヒストリ
        """
        histories = cmds.listHistory(mesh)
        sorted_histories = cmds.ls(histories, type=sort_type)
        if raise_ex_if_is_none:
            if sorted_histories == []:
                err_msg = Lang.pack(u'{}が存在しません。'.format(sort_type),
                                    '{} does not exist.'.format(sort_type),
                                    lang)
                raise UnexpectedError(err_msg)
        return sorted_histories