# -*- coding: utf-8 -*-
from ..util.readonly import metaclass


class Const(metaclass('Const')):
    TOOL_NAME   = 'HumBlendShapedMeshEditor'
    RUN_BUTTON  = 'RunButton'

    START_TEXT  = 'Start editing'
    START_ANNOTATION  = u'ベースメッシュを選択し、ボタンを押します。\nターゲットメッシュが削除され、メッシュ編集を開始します。'
    START_COLOR  = (0.4, 0.4, 0.4)

    FINISH_TEXT = 'Finish editing'
    FINISH_ANNOTATION = u'ベースメッシュを選択し、ボタンを押します。\nCVがフリーズされ、メッシュ編集を終了します。'
    FINISH_COLOR = (0.95, 0.95, 0.0)
