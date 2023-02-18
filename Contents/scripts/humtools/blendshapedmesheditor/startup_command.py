# -*- coding: utf-8 -*-

def bsme_startup_command():
    bsme_reload_modules()
    bsme_show_window()


def bsme_reload_modules():
    from humtools.blendshapedmesheditor import const, window, rebuilt_target_mesh_deleter, cv_freezer, uv_shifter, selection, \
        non_deformer_history_deleter, tweak_helper

    from humtools import module_reloader
    modules = [const, window, rebuilt_target_mesh_deleter, cv_freezer, uv_shifter, selection, \
                non_deformer_history_deleter, tweak_helper]
    module_reloader.reload_a_few_times(modules)


def bsme_show_window():
    from humtools.blendshapedmesheditor.window import Window
    from humtools.blendshapedmesheditor.const import Const
    wnd = Window(Const.TOOL_NAME)
    wnd.show()


if __name__ == '__main__':
    bsme_startup_command()
