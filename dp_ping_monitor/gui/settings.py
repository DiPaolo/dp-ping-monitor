import json
from enum import Enum
from typing import List, Optional

from PySide6.QtCore import QSettings


class SettingsKey(Enum):
    WINDOW_GEOMETRY = 'windowGeometry'
    WINDOW_STATE = 'windowState'
    SPLITTER_STATE = 'splitterState'

    LOG_WINDOW_GEOMETRY = 'logWindowGeometry'


def _get_settings():
    settings = QSettings()
    settings.setDefaultFormat(QSettings.Format.IniFormat)
    return settings


def get_settings_bool_value(key: SettingsKey, default: Optional[bool] = False):
    return _get_settings().value(key.value, default)


def set_settings_bool_value(key: SettingsKey, value: bool):
    _get_settings().setValue(key.value, value)


def get_settings_int_value(key: SettingsKey, default: Optional[int] = 0):
    return _get_settings().value(key.value, default)


def set_settings_int_value(key: SettingsKey, value: int):
    _get_settings().setValue(key.value, value)


def get_settings_float_value(key: SettingsKey, default: Optional[float] = 0):
    return _get_settings().value(key.value, default)


def set_settings_float_value(key: SettingsKey, value: float):
    _get_settings().setValue(key.value, value)


def get_settings_str_value(key: SettingsKey, default: Optional[str] = ''):
    return _get_settings().value(key.value, default)


def set_settings_str_value(key: SettingsKey, value: str):
    _get_settings().setValue(key.value, value)


def get_settings_list_value(key: SettingsKey, default: Optional[List] = None):
    if default is None:
        default = list()

    ret = _get_settings().value(key.value, '')
    if ret == '':
        return default

    return json.loads(ret)


def set_settings_list_value(key: SettingsKey, value: List):
    _get_settings().setValue(key.value, json.dumps(value))


def get_settings_byte_array_value(key: SettingsKey, default: Optional[bytes] = None):
    return _get_settings().value(key.value, default)


def set_settings_byte_array_value(key: SettingsKey, value: str):
    _get_settings().setValue(key.value, value)
