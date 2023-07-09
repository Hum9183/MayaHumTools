# -*- coding: utf-8 -*-
from maya import cmds, mel
import maya.api.OpenMaya as om2

from ..util.lang                import Lang
from ..util.unexpected_error    import UnexpectedError
from .lang_op_var               import LangOpVar


class Selection:
    def __init__(self):
        self.__sel_list = om2.MSelectionList()

    def get_meshes_as_sel_list(self):
        active_sel_list = om2.MGlobal.getActiveSelectionList()
        if active_sel_list.isEmpty():
            return self.__sel_list

        for index in range(active_sel_list.length()):
            self.__search_mesh_recursive(active_sel_list.getDagPath(index))

        if self.__sel_list.isEmpty():
            raise UnexpectedError(Lang.pack(u'スキンバインドされたメッシュを選択してください', 'Please Select skin bound meshes', LangOpVar.get()))

        return self.__sel_list

    def __search_mesh_recursive(self, dag_path):
        """meshを再帰的に走査する。見つけた場合はメンバのMSelectionListに追加する"""
        if self.__is_mesh_parent_transform(dag_path):
            self.__sel_list.add(dag_path)

        children_dag_paths = self.__get_children_dag_paths(dag_path)
        if len(children_dag_paths) == 0:
            return

        for child_dag_path in children_dag_paths:
            # 子がTransformなら再帰的に走査する
            if child_dag_path.apiType() == om2.MFn.kTransform:
                self.__search_mesh_recursive(child_dag_path)

    def __is_mesh_parent_transform(self, dag_path):
        """meshの親transformかどうか"""
        if dag_path.apiType() != om2.MFn.kTransform:
            return False

        # バインド済メッシュの親Transformなら、shapeとorigShapeの2つを子に持つ
        child_count = dag_path.childCount()
        if child_count != 2: 
            return False

        for index in range(child_count):
            child = dag_path.child(index)
            if child.apiType() != om2.MFn.kMesh:
                return False

        return True

    def __get_children_dag_paths(self, dag_path):
        """子をMDagPathArrayで返す"""
        child_count = dag_path.childCount()
        children_dag_paths = om2.MDagPathArray()
        for index in range(child_count):
            child_m_object = dag_path.child(index)
            children_dag_paths.append(om2.MDagPath.getAPathTo(child_m_object))
        return children_dag_paths
