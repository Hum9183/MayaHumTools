# -*- coding: utf-8 -*-
from textwrap import dedent

import maya.cmds as cmds


def __register_humtools_startup():
    cmd = dedent(
        """
        import humtools.startup
        humtools.startup.execute()
        """)
    cmds.evalDeferred(cmd)


if __name__ == '__main__':
    try:
        __register_humtools_startup()

    except Exception as e:
        import traceback
        traceback.print_exc()
