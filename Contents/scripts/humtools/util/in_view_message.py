# -*- coding: utf-8 -*-
from maya import cmds

from .log import Log


def show(message, fadeStayTime=3000):
    highlighted_msg = u'<hl>{}</hl>'.format(message)
    cmds.inViewMessage(amg=highlighted_msg, pos='botCenter', fade=True, fst=fadeStayTime)
    Log.log(message)