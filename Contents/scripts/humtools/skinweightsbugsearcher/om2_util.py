# -*- coding: utf-8 -*-
import maya.api.OpenMaya as om2


# NOTE: 仮置き
def get_skincluster_node(mesh_depend_node):
    dg_iterator = om2.MItDependencyGraph(
                    mesh_depend_node,
                    om2.MFn.kSkinClusterFilter,    # NOTE: kInvalidを渡すと無指定になるので全て列挙することもできる
                    om2.MItDependencyGraph.kUpstream)
    while not dg_iterator.isDone():
        m_object = dg_iterator.currentNode()
        if m_object.hasFn(om2.MFn.kSkinClusterFilter):
            return m_object
        dg_iterator.next()
    return None


def get_influence_names(skinclister_fn):
    infl_dag_paths = skinclister_fn.influenceObjects()
    infl_count = len(infl_dag_paths)

    infl_short_names = []
    for i in range(infl_count):
        # ショートネームを取得する
        infl_depend_node = infl_dag_paths[i].node()
        dn_fn = om2.MFnDependencyNode(infl_depend_node)
        infl_short_names.append(dn_fn.name())   

    return infl_short_names
