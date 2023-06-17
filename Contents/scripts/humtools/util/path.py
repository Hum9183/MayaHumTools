# -*- coding: utf-8 -*-
import os

from ..hum_tools_const import HumToolsConst


def combine(paths):
    """パスのlistを結合し、パスを返す。

    Args:
        paths (list[str]): パスのlist

    Returns:
        str: \で結合したパス。
    """
    return '\\'.join(paths)


def get_humtools_app_data_folder_path():
    """HumToolsのAppDataのフォルダパスを取得する。

    Returns:
        str: HumToolsのAppDataのフォルダパス
    """
    home_path = '{}{}'.format(os.getenv('HOMEDRIVE'), os.getenv('HOMEPATH'))
    maya_hum_tools = 'Maya{}'.format(HumToolsConst.HUM_TOOLS)
    folder_names = [home_path, 'AppData', 'Local', maya_hum_tools]
    return combine(folder_names)


def create_folder_recursive(path):
    """フォルダを作成する。中間ディレクトリもすべて作成する。

    Args:
        path (str): 作成するフォルダのパス
    """
    if os.path.isdir(path):
        return

    folder_names = path.split('\\')

    # すべてのフォルダパスのリストを作成
    folder_paths = []
    for _ in range(len(folder_names)):
        folder_path = combine(folder_names)
        folder_paths.append(folder_path)
        del folder_names[-1]

    # フォルダ作成
    for _folder_path in reversed(folder_paths):
        if os.path.isdir(_folder_path) is False:
            os.mkdir(_folder_path)