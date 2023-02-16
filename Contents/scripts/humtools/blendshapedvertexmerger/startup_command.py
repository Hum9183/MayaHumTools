# -*- coding: utf-8 -*-

def bsvm_startup_command():
    bsvm_reload_modules()
    bsvm_show_window()


def bsvm_reload_modules():
    from humtools.blendshapedvertexmerger import const, window, main, selected_getter, \
        blendshape_target_rebuilder, vtx_merger, non_deformer_history_deleter, blendshape_reconfigurator

    from humtools import module_reloader
    modules = [const, window, main, selected_getter, blendshape_target_rebuilder, \
                vtx_merger, non_deformer_history_deleter, blendshape_reconfigurator]
    module_reloader.reload_py_ver(modules)


def bsvm_show_window():
    from humtools.blendshapedvertexmerger.window import Window
    from humtools.blendshapedvertexmerger.const import Const
    wnd = Window(Const.TOOL_NAME)
    wnd.show()


if __name__ == '__main__':
    bsvm_startup_command()
