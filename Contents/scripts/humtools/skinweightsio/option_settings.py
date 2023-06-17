# -*- coding: utf-8 -*-
import json
import os
from textwrap import dedent

from maya import cmds

from ..util.log import Log
from .const import Const

class OptionSettings:
    def __init__(self, json_path):
        self.__json_path = json_path

        self.import_method     = ''
        self.ignore_name       = None
        self.normalize_weights = None
        self.auto_binding      = None

    def create(self):
        if os.path.isfile(self.__json_path):
            return
        else:
            self.__create_init()

    def overwrite(self):
        new_option_settings_dict = {
            Const.KEY_IMPORT_METHOD     : self.import_method,
            Const.KEY_IGNORE_NAME       : self.ignore_name,
            Const.KEY_NORMALIZE_WEIGHTS : self.normalize_weights,
            Const.KEY_AUTO_BINDING      : self.auto_binding,
        }
        self.__save_json(new_option_settings_dict)

    def load(self):
        text_io_wrapper = open(self.__json_path)
        option_settings_json = json.load(text_io_wrapper)

        self.import_method     = option_settings_json[Const.KEY_IMPORT_METHOD]
        self.ignore_name       = option_settings_json[Const.KEY_IGNORE_NAME]
        self.normalize_weights = option_settings_json[Const.KEY_NORMALIZE_WEIGHTS]
        self.auto_binding      = option_settings_json[Const.KEY_AUTO_BINDING]

    def reset(self):
        self.__create_init()
        self.load()

    def __save_json(self, dict):
        text_io_wrapper = open(self.__json_path , 'w')
        json.dump(dict, text_io_wrapper, indent=4)

    def __create_init(self):
        init_option_settings_dict = {
            Const.KEY_IMPORT_METHOD     : Const.METHOD_INDEX,
            Const.KEY_IGNORE_NAME       : False,
            Const.KEY_NORMALIZE_WEIGHTS : True,
            Const.KEY_AUTO_BINDING      : True,
        }
        self.__save_json(init_option_settings_dict)

    def set_import_method(self, import_method):
        self.import_method = import_method
        self.overwrite()

    def toggle_ignore_name(self):
        self.ignore_name = not self.ignore_name
        self.overwrite()

    def toggle_normalize_weights(self):
        self.normalize_weights = not self.normalize_weights
        self.overwrite()

    def toggle_auto_binding(self):
        self.auto_binding = not self.auto_binding
        self.overwrite()

    def log(self):
        text = dedent(
            u"""
                # OptionSettings
                # import_method     ...{}
                # ignore_name       ...{}
                # normalize_weights ...{}
                # auto_binding      ...{}
            """
            .format(
                self.import_method,
                self.ignore_name,
                self.normalize_weights,
                self.auto_binding)
        )
        Log.log(text)

