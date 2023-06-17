# -*- coding: utf-8 -*-
from ..util.readonly import metaclass


class Const(metaclass('Const')):
    TOOL_NAME = 'HumSkinWeightsIO'
    XMLS_FOLDER_NAME = 'XMLs'
    OPTION_SETTINGS_FOLDER_NAME = 'OptionSettings'
    OPTION_SETTINGS_JSON_NAME   = 'option_settings'

    XML_TEXT_SCROLL_LIST_NAME = 'HumSWIO_XMLTextScrollList'

    # Option settings json keys
    KEY_IMPORT_METHOD     = 'importMethod'
    KEY_IGNORE_NAME       = 'ignoreName'
    KEY_NORMALIZE_WEIGHTS = 'normalizeWeights'
    KEY_AUTO_BINDING      = 'autoBinding'

    # Import methods
    METHOD_INDEX   = 'index'
    METHOD_OVER    = 'over'
    METHOD_NEAREST = 'nearest'
