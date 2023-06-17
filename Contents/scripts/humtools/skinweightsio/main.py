# -*- coding: utf-8 -*-
from ..util.lang                import Lang
from ..util.unexpected_error    import UnexpectedError
from ..util                     import dict_util
from ..util                     import in_view_message
from .auto_skin_binder          import AutoSkinBinder
from .deformer_weights_exporter import DeformerWeightsExporter
from .deformer_weights_importer import DeformerWeightsImporter
from .lang_op_var               import LangOpVar
from .selection                 import Selection
from .                          import mesh_parent_transform_and_skincluster_dict_getter


@UnexpectedError.catch
def create_xml(xmls_folder_path, xml_text_scroll_list):
    # NOTE: 名前被り対策はしていない
    selection = Selection()
    mesh_parent_transforms = selection.get_mesh_parent_transforms()

    mesh_parent_transform_and_skincluster_dict = mesh_parent_transform_and_skincluster_dict_getter.get_for_export(mesh_parent_transforms)

    deformer_weights_exporter = DeformerWeightsExporter(xmls_folder_path, xml_text_scroll_list)
    deformer_weights_exporter.export_xmls(mesh_parent_transform_and_skincluster_dict)

    __show_completion_message()


@UnexpectedError.catch
def copy_weights(xmls_folder_path, option_settings):
    selection = Selection()
    mesh_parent_transforms = selection.get_mesh_parent_transforms()
    mesh_parent_transform_and_skincluster_dict = mesh_parent_transform_and_skincluster_dict_getter.get_for_import(mesh_parent_transforms)

    if option_settings.auto_binding:
        auto_skin_binder = AutoSkinBinder(xmls_folder_path, mesh_parent_transform_and_skincluster_dict)
        auto_skin_binder.bind()
        mesh_parent_transform_and_skincluster_dict = auto_skin_binder.get_dict_skin_bound() # WARNING: 再代入

    transform_and_skincluster_dict_normalized = dict_util.delete_elements_with_the_value_none(mesh_parent_transform_and_skincluster_dict)
    if len(transform_and_skincluster_dict_normalized) == 0:
        __raise_copy_weights_err()

    deformer_weights_importer = DeformerWeightsImporter(xmls_folder_path, option_settings)
    deformer_weights_importer.import_xmls(transform_and_skincluster_dict_normalized)

    __show_completion_message()


def __raise_copy_weights_err():
    ja_JP = (u"""ウェイトのコピーができませんでした。以下を試してください。
    ・skinClusterを持つメッシュを選択する。
    ・自動バインドオプションを有効にする。
    ・同名のXMLファイルが作成する。""")

    en_US = ("""Could not copy weights. Try the following:
    -Select the meshes that has skinCluster.
    -Enable the Auto binding option.
    -Create XML file with the same name.""")

    err_msg = Lang.pack(ja_JP, en_US, LangOpVar.get())
    raise UnexpectedError(err_msg)


def __show_completion_message():
    in_view_message.show(Lang.pack(u"処理が完了しました。", 'The process has been completed.', LangOpVar.get()))