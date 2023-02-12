# -*- coding: utf-8 -*-
from textwrap import dedent

from maya import cmds
from .const import Const

from .. import menu_adder


def setup():
    # NOTE: シェルフに登録できるようにするために、起動コマンドはstringで渡す

    blendshaped_vertex_merger_startup_command = dedent('''
        def bvms_startup_command():
            bvms_reload_modules()
            bvms_show_window()


        def bvms_reload_modules():
            from humtools.blendshapedvertexmerger import const, window, main, \
                selected_getter, blendshape_target_rebuilder, vtx_merger, non_deformer_history_deleter

            from humtools import module_reloader
            modules = [const, window, main, \
                selected_getter, blendshape_target_rebuilder, vtx_merger, non_deformer_history_deleter]
            module_reloader.reload_a_few_times(modules)


        def bvms_show_window():
            from humtools.blendshapedvertexmerger.window import Window # reload後は再importする必要がある
            from humtools.blendshapedvertexmerger.const import Const
            wnd = Window(Const.TOOL_NAME)
            wnd.show()


        bvms_startup_command()
    ''')

    menu_adder.add(Const.TOOL_NAME, blendshaped_vertex_merger_startup_command)