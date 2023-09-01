import datetime

from PySide6.QtWidgets import QTableWidgetItem

from dp_ping_monitor.config import config

_log_widget = None


def set_log_widget(w: QTableWidgetItem):
    global _log_widget
    _log_widget = w


def error(msg: str):
    print(f'[ERROR]   {msg}')
    if _log_widget:
        _add_to_log_tree_widget(datetime.datetime.now(), 'Error', msg)


def info(msg: str):
    print(f'[INFO]    {msg}')
    if _log_widget:
        _add_to_log_tree_widget(datetime.datetime.now(), 'Info', msg)


def debug(msg: str):
    if config.is_debug:
        print(f'[DEBUG]   {msg}')
        if _log_widget:
            _add_to_log_tree_widget(datetime.datetime.now(), 'Debug', msg)


def _add_to_log_tree_widget(dt: datetime.datetime, severity: str, msg: str):
    count = _log_widget.rowCount()
    _log_widget.insertRow(count)
    _log_widget.setItem(count, 0, QTableWidgetItem(str(dt)))
    _log_widget.setItem(count, 1, QTableWidgetItem(severity))
    _log_widget.setItem(count, 2, QTableWidgetItem(msg))
