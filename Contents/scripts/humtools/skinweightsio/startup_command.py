# -*- coding: utf-8 -*-

def swio_startup_command():
    swio_reload_modules()
    swio_show_window()


def swio_reload_modules():
    from humtools.skinweightsio import const, window, selection, auto_skin_binder, mesh_parent_transform_and_skincluster_dict_getter, \
        deformer_weights_exporter, deformer_weights_importer, main, xml_text_scroll_list, option_settings, lang_op_var

    from humtools import module_reloader
    modules = [const, window, selection, auto_skin_binder, mesh_parent_transform_and_skincluster_dict_getter, \
                deformer_weights_exporter, deformer_weights_importer, main, xml_text_scroll_list, option_settings, lang_op_var]
    module_reloader.reload_a_few_times(modules)


def swio_show_window():
    from humtools.skinweightsio.window import Window
    from humtools.skinweightsio.const import Const
    wnd = Window(Const.TOOL_NAME)
    wnd.show()


if __name__ == '__main__':
    swio_startup_command()
