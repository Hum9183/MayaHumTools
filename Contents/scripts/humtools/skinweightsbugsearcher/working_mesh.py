# -*- coding: utf-8 -*-
from maya import cmds, mel
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as oma2

from ..util.lang                import Lang
from ..util.unexpected_error    import UnexpectedError
from .lang_op_var               import LangOpVar
from .                          import om2_util


class WorkingMesh:
    @staticmethod
    def create_from_sel_list(sel_list):
        working_meshes = []

        for index in range(sel_list.length()):
            m_object_dn = sel_list.getDependNode(index)
            name = om2.MFnDependencyNode(m_object_dn).name()
            dag_path, m_object_component = sel_list.getComponent(index)

            working_mesh = WorkingMesh(name, dag_path, m_object_component)
            if working_mesh.initialize():
                working_meshes.append(working_mesh)

        if working_meshes == []:
            raise UnexpectedError(Lang.pack(u'スキンバインドされたメッシュを選択してください', 'Please Select skin bound meshes', LangOpVar.get()))

        return working_meshes

    def __init__(self, name, dag_path, m_object_component):
        self.name                 = name                # type: str
        self.vert_count           = None                # type: int
        self.mesh_vert_it_main    = None                # type: om2.MItMeshVertex
        self.__mesh_vert_it_sub   = None                # type: om2.MItMeshVertex
        self.__mesh_poly_it       = None                # type: om2.MItMeshPolygon
        self.__dag_path           = dag_path            # type: om2.MDagPath
        self.__mesh_dag_path      = None                # type: om2.MDagPath
        self.__m_object_component = m_object_component  # type: om2.MDagPath # (component)
        self.__skincluster_fn     = None                # type: oma2.MFnSkinCluster
        self.__influences_names   = None                # type: list[str]
        self.__influences_count   = None                # type: int

    def initialize(self):
        # mesh dag path
        self.__mesh_dag_path = self.__dag_path.extendToShape()

        # skincluster
        skincluster_node = om2_util.get_skincluster_node(self.__mesh_dag_path.node())
        if skincluster_node is None:
            return False
        self.__skincluster_fn = oma2.MFnSkinCluster(skincluster_node)

        # influences
        self.__influences_names = om2_util.get_influence_names(self.__skincluster_fn)
        self.__influences_count = len(self.__influences_names)

        # iterator mesh
        temp_dag_path = self.__dag_path
        temp_m_object_component = self.__m_object_component
        self.mesh_vert_it_main  = om2.MItMeshVertex(temp_dag_path, temp_m_object_component)
        self.__mesh_vert_it_sub = om2.MItMeshVertex(temp_dag_path, temp_m_object_component)
        self.__mesh_poly_it     = om2.MItMeshPolygon(temp_dag_path, temp_m_object_component)

        # vertex count
        self.vert_count = self.mesh_vert_it_main.count()

        return True

    def get_current_vert_id(self):
        return int(self.mesh_vert_it_main.index())

    def get_current_vert_skinweights(self):
        MD_ARRAY_INDEX = 0
        return self.__skincluster_fn.getWeights(self.__mesh_dag_path, self.__get_current_vert_component())[MD_ARRAY_INDEX]

    def get_vert_ids_nearby_current_vert(self):
        """current頂点の「近くの頂点のID」を取得する"""
        nearby_vert_ids = []
        face_ids = self.mesh_vert_it_main.getConnectedFaces() # NOTE: Faceで繋がっているものを取得する

        for face_id in face_ids:
            self.__mesh_poly_it.setIndex(face_id)
            vert_ids = self.__mesh_poly_it.getVertices()
            nearby_vert_ids.extend(vert_ids)

        nearby_vert_ids = list(set(nearby_vert_ids))
        nearby_vert_ids.remove(self.get_current_vert_id()) # NOTE: 自身は消す

        return nearby_vert_ids

    def calc_infl_vaild_nearby_verts(self, nearby_vert_ids):
        """周囲の頂点の「ウェイトが振られているインフルエンスリスト」を作成する"""
        MD_ARRAY_INDEX = 0
        all_infl_valid = [False] * self.__influences_count

        for nearby_vert_id in nearby_vert_ids:
            # NOTE: mesh_vert_it_mainは頂点走査のメインループで使用しているため、subのイテレータを使用する
            self.__mesh_vert_it_sub.setIndex(nearby_vert_id)
            component = self.__mesh_vert_it_sub.currentItem()
            nearby_vert_weights = self.__skincluster_fn.getWeights(self.__mesh_dag_path, component)[MD_ARRAY_INDEX]
            nearby_vert_infl_valid = self.__calc_influences_valid(nearby_vert_weights)
            all_infl_valid = [all or nearby for all, nearby in zip(all_infl_valid, nearby_vert_infl_valid)] # WARNING: 再代入

        return all_infl_valid

    def calc_unexpected_influeces(self, skinweights, nearby_vert_infl_valid):
        """「周囲の頂点ではウェイトが振られていない骨」にウェイトが振られているかを計算する。
            振られていた骨名のリストを返す。
        """
        current_infl_valid = self.__calc_influences_valid(skinweights)
        unexpected_infl_valid = [(current is True) and (nearby is False) for current, nearby in zip(current_infl_valid, nearby_vert_infl_valid)]
        unexpected_infl_names = [name for vaild, name in zip(unexpected_infl_valid, self.__influences_names) if vaild]
        return unexpected_infl_names

    def __get_current_vert_component(self):
        return self.mesh_vert_it_main.currentItem()

    def __calc_influences_valid(self, skin_weights):
        """ウェイトが振られているかどうかのリストを返す"""
        return [skin_weight > 0 for skin_weight in skin_weights]

    # NOTE: 処理の備忘録
    # def select_current_vert(self):
    #     sel_list = om2.MSelectionList()
    #     vert_tuple = (self.__dag_path, self.get_current_vert_component())
    #     sel_list.add(vert_tuple)
    #     om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectComponentMode)
    #     om2.MGlobal.setActiveSelectionList(sel_list)
