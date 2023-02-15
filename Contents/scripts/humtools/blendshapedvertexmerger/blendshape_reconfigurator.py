# -*- coding: utf-8 -*-
from maya import cmds

from ..lib import blendshape


class BlendShapeReconfigurator:
    def __init__(self, reconfigure_bs_setting, base_mesh, bs_nodes):
        self.__reconfigure_bs_setting = reconfigure_bs_setting
        self.__base_mesh              = base_mesh
        self.__bs_nodes               = bs_nodes
        self.__preserved_bs_dict      = dict()  # dict{str, list[(long, str)]}

    def preserve(self):
        if not self.__reconfigure_bs_setting:
            return
        blendshape.exists_validate(self.__bs_nodes)
        self.__preserved_bs_dict = {bs: blendshape.get_targets_tuples(bs) for bs in self.__bs_nodes}

    def delete_nodes(self):
        if not self.__reconfigure_bs_setting:
            return
        blendshape.exists_validate(self.__bs_nodes)
        cmds.delete(self.__bs_nodes)

    def configure(self):
        if not self.__reconfigure_bs_setting:
            return
        blendshape.exists_validate(self.__bs_nodes)
        self.__create_blendshapes()
        self.__create_blendshape_targets()

    def __create_blendshapes(self):
        base_mesh = self.__base_mesh
        for bs_node, _ in self.__preserved_bs_dict.items():
            cmds.blendShape(base_mesh, n=bs_node)

    def __create_blendshape_targets(self):
        base_mesh = self.__base_mesh
        for bs_node, bs_tuple in self.__preserved_bs_dict.items():
            for idx, target in bs_tuple:
                cmds.blendShape(bs_node, e=True, t=(base_mesh, idx, target, 1))