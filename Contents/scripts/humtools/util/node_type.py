# -*- coding: utf-8 -*-
from maya import cmds

from ..util.readonly import metaclass
from ..util.unexpected_error import UnexpectedError


class NodeType(metaclass('NodeType')):
    BLEND_SHAPE = 'blendShape'
    MESH        = 'mesh'
    TWEAK       = 'tweak'

    @staticmethod
    def get_histories(mesh, sort_type, raise_ex_if_is_none=False):
        histories = cmds.listHistory(mesh)
        sorted_histories = cmds.ls(histories, type=sort_type)
        if raise_ex_if_is_none:
            if sorted_histories == []:
                raise UnexpectedError(u'{}が存在しません。'.format(sort_type))
        return sorted_histories