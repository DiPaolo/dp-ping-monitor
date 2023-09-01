import datetime

from PySide6 import QtCore
from PySide6.QtCore import Slot, Signal, QTimer, QThread
from PySide6.QtWidgets import QDialog

from dp_ping_monitor import __version__
from dp_ping_monitor.config import config
from dp_ping_monitor.core import ping_output_parser
from dp_ping_monitor.core.ping_stats import PingStats
from dp_ping_monitor.core.process_monitor import ProcessMonitor
from dp_ping_monitor.gui import logger, settings
from dp_ping_monitor.gui.log_window import LogWindow
from dp_ping_monitor.gui.settings import SettingsKey
from dp_ping_monitor.gui.ui.ui_main_dialog import Ui_Dialog


class MainDialog(QDialog):
    started = Signal()
    stopped = Signal()

    _started_time = None

    _ping_stats = PingStats()

    _thread = None
    _worker = None
    _timer = None
    _proc_mon = None

    def __init__(self):
        super(MainDialog, self).__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle(f'{config.application_name} {config.app_version.as_str(2)}')

        self.log_window = LogWindow(self)
        # self.log_window.visibility_changed.connect(self.ui.show_log_window.setChecked)
        # self.log_window.show()

        logger.info('Application starting...')

        # restore position and state
        self.setWindowState(settings.get_settings_byte_array_value(SettingsKey.WINDOW_STATE, QtCore.Qt.WindowNoState))
        self.restoreGeometry(settings.get_settings_byte_array_value(SettingsKey.WINDOW_GEOMETRY))

        #
        # connections
        #

        # # log window
        # self.ui.show_log_window.toggled.connect(lambda checked: self.log_window.setVisible(checked))
        # self.ui.show_log_window.setChecked(True)

        [elem.textChanged.connect(self._update_start_stop_status) for elem in [
            # self.ui.username, self.ui.token
        ]]

        # start/stop + exit
        self.ui.start_stop.clicked.connect(self._start_ping)

        #
        # initialization of controls
        #

        self._update_stats_controls()

        # after connections!
        # after stats is set to correctly enable/disable some controls
        self._init_controls()

    def closeEvent(self, event):
        logger.info('Exiting application...')

        self._cancel_ping()

        # save window position and size
        settings.set_settings_byte_array_value(SettingsKey.WINDOW_GEOMETRY, self.saveGeometry())
        settings.set_settings_byte_array_value(SettingsKey.WINDOW_STATE, self.windowState())

        event.accept()

    def _init_controls(self):
        # username = settings.get_settings_str_value(SettingsKey.USERNAME, getpass.getuser())
        # self.ui.username.setText(username)
        #
        # out_image_path = settings.get_settings_str_value(SettingsKey.OUT_IMAGE_PATH, config.defaults.out_image_path)
        # abs_out_image_path = os.path.abspath(out_image_path)
        # self.ui.output_folder.setText(abs_out_image_path)
        #
        # out_image_name = settings.get_settings_str_value(SettingsKey.OUT_IMAGE_BASE_NAME,
        #                                                  config.defaults.out_image_base_name)
        # self.ui.image_filename_template.setText(out_image_name)
        #
        # min_percent = settings.get_settings_float_value(SettingsKey.MIN_PERCENT, config.defaults.min_percent)
        # self.ui.min_percent.setValue(min_percent)

        self._init_about_program()

    def _init_about_program(self):
        self.ui.program_name_n_version.setText(
            f'<p style="color:gray;">'
            f'{config.application_name} {config.app_version.as_str(4)}'
            f'</p>'
        )

        self.ui.copyright.setText(
            f"<p style='color:gray;'>"
            f"Copyright 2023 {__version__.__author__} "
            f"(<a href='mailto:{__version__.__author_email__}'>{__version__.__author_email__}</a>)"
            f"</p>"
        )

    def _update_start_stop_status(self):
        elems = [
            # self.ui.username, self.ui.token
        ]
        filled_elem_count = list(filter(lambda elem: len(elem.text()) > 0, elems))
        self.ui.start_stop.setEnabled(len(filled_elem_count) == len(elems))

    @Slot()
    def _start_ping(self):
        self._cancel_ping()

        logger.info('Start collecting statistics...')

        self._ping_stats.reset()

        self._set_all_controls_enabled(False)

        self._started_time = datetime.datetime.now()
        self.started.emit()

        self.ui.start_stop.setText('Cancel')
        self.ui.start_stop.clicked.disconnect()
        self.ui.start_stop.clicked.connect(self._cancel_ping)

        self._proc_mon = ProcessMonitor('ping', ['google.com'])
        self._proc_mon.start()

        self._thread = QThread()
        # self._worker = ThreadWorker('', '')
        # self._worker.moveToThread(self._thread)
        # self._worker.started.connect(self.started)
        # self._worker.finished.connect(self._stop_ping)

        # self._thread.started.connect(self._worker.run)

        self._thread.start()

        self._timer = QTimer()
        self._timer.timeout.connect(self._update_cur_stats)
        self._timer.start(1000)

        logger.info('Pinging started')

    @Slot()
    def _cancel_ping(self):
        self._stop_ping(False)

    @Slot()
    def _stop_ping(self, done: bool = True):
        """

        :param done: done/finished if True; canceled if False
        :return:
        """

        logger.info(f"{'Finishing' if done else 'Stopping'} pinging...")

        if self._timer:
            self._timer.stop()
            self._timer = None

        if self._worker:
            # use it as the current stats if done + update cache
            if done:
                # self._set_stats(datetime.datetime.utcnow(), self._worker.cur_stats)
                # cache.save_stats(self._stats_datetime_utc, self._stats)
                # self._update_cur_stats_info()
                pass

            self._worker.stop()

        if self._proc_mon:
            self._proc_mon.stop()
            self._proc_mon = None
            # self._worker = None

        if self._thread:
            self._thread.quit()
            self._thread.wait()
            self._thread = None

        self._started_time = None
        self._set_all_controls_enabled(True)
        self.stopped.emit()

        self.ui.start_stop.setText('Start')
        self.ui.start_stop.clicked.disconnect()
        self.ui.start_stop.clicked.connect(self._start_ping)

        logger.info(f"Pinging {'done' if done else 'canceled'}")

    def _is_pinging(self) -> bool:
        return self._thread is not None and self._thread.isRunning()

    def _set_all_controls_enabled(self, enabled: bool = True):
        [elem.setEnabled(enabled) for elem in [
            # self.ui.username, self.ui.token, self.ui.image_filename_template, self.ui.choose_out_image_dir
        ]]

    @Slot()
    def _update_cur_stats(self):
        # self.ui.stats_status.setText(f'<p style="color:green;">Statistics Ready (gen. {gen_datetime_str})</p')
        cli_ret_code = self._proc_mon.is_cli_done()
        lines = self._proc_mon.lines if self._proc_mon else []
        # print(lines)
        for line in lines:
            cur_ping = ping_output_parser.parse_line(line)
            print(cur_ping)
            if cur_ping is not None:
                self._ping_stats.add(cur_ping)

        self._update_stats_controls()

    def _update_stats_controls(self):
        if self._started_time:
            self.ui.start_time.setText(self._started_time.strftime('%Y-%m-%d %H:%M:%S'))

            duration = datetime.datetime.now() - self._started_time
            dur_left = duration.seconds

            days = dur_left // (24 * 3600)
            dur_left = dur_left % (24 * 3600)

            hours = dur_left // 3600
            dur_left = dur_left % 3600

            mins = dur_left // 60
            dur_left = dur_left % 60

            secs = dur_left

            duration_str = ''
            if days > 0:
                duration_str += f'{days}d '
            if hours > 0:
                duration_str += f'{hours:02}h '
            if mins > 0:
                duration_str += f'{mins:02}m '
            duration_str += f'{secs:02}s'

            self.ui.duration.setText(duration_str)
        else:
            self.ui.start_time.setText('not started')
            self.ui.duration.setText('not started')

        self.ui.avg_ping.setText(f'{self._ping_stats.avg:.02f}')
        self.ui.min_ping.setText(str(self._ping_stats.min))
        self.ui.max_ping.setText(str(self._ping_stats.max))
