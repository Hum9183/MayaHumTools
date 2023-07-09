# -*- coding: utf-8 -*-


def swbs_startup_command():
    swbs_reload_modules()
    swbs_show_window()


def swbs_reload_modules():
    from humtools.skinweightsbugsearcher import const, window, bug_searcher, working_mesh, weights_bug_text_scroll_list, om2_util, selection
    from humtools import module_reloader
    modules = [const, window, bug_searcher, working_mesh, weights_bug_text_scroll_list, om2_util, selection]
    module_reloader.reload_a_few_times(modules)


def swbs_show_window():
    from humtools.skinweightsbugsearcher.const  import Const
    from humtools.skinweightsbugsearcher.window import Window
    wnd = Window(Const.TOOL_NAME)
    wnd.show()


if __name__ == '__main__':
    swbs_startup_command()
