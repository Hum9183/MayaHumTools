# -*- coding: utf-8 -*-
from textwrap import dedent

from maya import cmds
from .const import Const

from .. import menu_adder


def add_menu():
    # NOTE: シェルフに登録できるようにするために、起動コマンドはstringで渡す

    # TODO: ファイルをテキストとして読み出すことは可能なので、普通の.pyとして書いて、
    # 使うときにテキストとして読み出して使うかたちでやってみる。.pyのほうがシンタックスハイライトがあって見やすい。
    # inspect を使ってもうまくできるかもしれない

    blendshaped_vertex_merger_startup_command = dedent('''
        def bsvm_startup_command():
            bsvm_reload_modules()
            bsvm_show_window()


        def bsvm_reload_modules():
            from humtools.blendshapedvertexmerger import const, window, main, \
                selected_getter, blendshape_target_rebuilder, vtx_merger, non_deformer_history_deleter, blendshape_reconfigurator

            from humtools import module_reloader
            modules = [const, window, main, \
                selected_getter, blendshape_target_rebuilder, vtx_merger, non_deformer_history_deleter, blendshape_reconfigurator]
            module_reloader.reload_py_ver(modules)


        def bsvm_show_window():
            from humtools.blendshapedvertexmerger.window import Window # reload後は再importする必要がある
            from humtools.blendshapedvertexmerger.const import Const
            wnd = Window(Const.TOOL_NAME)
            wnd.show()


        bsvm_startup_command()
    ''')

    menu_adder.add(Const.TOOL_NAME, blendshaped_vertex_merger_startup_command)