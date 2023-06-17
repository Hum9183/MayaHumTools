# -*- coding: utf-8 -*-
from maya import cmds

from ..util.lang             import Lang
from ..util.node_type        import NodeType
from ..util.unexpected_error import UnexpectedError
from .lang_op_var            import LangOpVar

class Selection:
    def __init__(self):
        self.__mesh_parent_transforms = []

    def get_mesh_parent_transforms(self):
        sels = cmds.ls(sl=True)
        self.__exists_validation(sels)
        [self.__get_mesh_parent_transform_recursive(s) for s in sels]
        return self.__mesh_parent_transforms

    def __exists_validation(self, sels):
        if sels == []:
            raise UnexpectedError(Lang.pack(u'メッシュを選択してください。', 'Please select the meshes.', LangOpVar.get()))

    def __get_mesh_parent_transform_recursive(self, node):
        """meshの親transformを再帰的に走査する。
            見つけた場合、メンバにappendする。
        """
        if self.__is_mesh_parent_transform(node):
            self.__mesh_parent_transforms.append(node)

        children = self.__get_children(node)
        if children is None:
            return

        for child in children:
            if self.__is_mesh(child): # nodeの子供のmeshは走査する必要がないためcontinueする。
                continue
            self.__get_mesh_parent_transform_recursive(child)

    def __is_mesh_parent_transform(self, node):
        shape = self.__get_child_shape(node)
        if shape is None:
            return False
        if self.__is_mesh(shape) is False: # NOTE: カメラやロケータではないかの確認
            return False
        return True

    def __get_children(self, node):
        return cmds.listRelatives(node, children=True, noIntermediate=True)

    def __get_child_shape(self, node):
        try:
            shapes = cmds.listRelatives(node, shapes=True, noIntermediate=True)
        except TypeError: # NOTE: NoneではなくTypeErrorが返ってくることがある
            return None
        if shapes is None:
            return None
        if len(shapes) >= 2:
            err_msg = Lang.pack(u'{}がシェイプである子供を2つ以上持っています。'.format(node),
                            '{} has two or more children that are mesh.'.format(node),
                            LangOpVar.get())
            raise UnexpectedError(err_msg)
        return shapes[0] 

    def __is_mesh(self, node):
        return cmds.nodeType(node) == NodeType.MESH
