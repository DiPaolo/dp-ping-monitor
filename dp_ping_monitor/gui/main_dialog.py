import datetime
from typing import List

from PySide6 import QtCore, QtCharts, QtGui
from PySide6.QtCore import Slot, Signal, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QSystemTrayIcon, QMenu

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

        self.ui.recent_servers.currentIndexChanged.connect(self._on_cur_server_changed)
        self.ui.graph_visible_interval.currentIndexChanged.connect(self._change_graph_visible_interval)

        # start/stop + exit
        self.ui.start_stop.clicked.connect(self._start_ping)

        #
        # init system tray icon
        #
        self.tray_icon = QSystemTrayIcon(QIcon(':/icons/app_icon.png'))
        self.tray_icon.activated.connect(self._on_tray_icon_activated)
        self.tray_icon.show()
        # self.started.connect(
        #     lambda: self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogYesButton)))
        # self.stopped.connect(
        #     lambda: self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogNoButton)))

        self.tray_context_menu = self._create_tray_context_menu()

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

    def _create_tray_context_menu(self) -> QMenu:
        menu = QMenu(self)
        start_action = menu.addAction('Start')
        stop_action = menu.addAction('Stop')
        menu.addSeparator()
        quit_action = menu.addAction('Quit')

        start_action.triggered.connect(self._start_ping)
        stop_action.triggered.connect(self._cancel_ping)
        quit_action.triggered.connect(self.close)

        def update_start_stop_actions():
            print(f'is pinging={self._is_pinging()}')
            start_action.setEnabled(not self._is_pinging())
            stop_action.setEnabled(self._is_pinging())

        self.started.connect(update_start_stop_actions)
        self.stopped.connect(update_start_stop_actions)

        # initial state
        update_start_stop_actions()

        return menu

    @Slot(QSystemTrayIcon.ActivationReason)
    def _on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # show/hide main window
            self.hide() if self.isVisible() else self.show()
        elif reason == QSystemTrayIcon.ActivationReason.Context:
            # show context menu
            self.tray_context_menu.popup(QtGui.QCursor.pos())

    def _init_controls(self):
        servers = settings.get_settings_list_value(SettingsKey.RECENT_SERVERS, [])
        if len(servers) == 0:
            servers = config.defaults.servers

        self.ui.recent_servers.addItems(servers)

        self._init_graph_view()
        self._init_graph_visible_interval()  # after _init_graph_view() because it needs self.axis_x
        self._init_about_program()

    def _init_graph_visible_interval(self):
        self.ui.graph_visible_interval.addItem('1 min', 60)
        self.ui.graph_visible_interval.addItem('5 mins', 5 * 60)
        self.ui.graph_visible_interval.addItem('10 mins', 10 * 60)
        self.ui.graph_visible_interval.addItem('15 mins', 15 * 60)
        self.ui.graph_visible_interval.addItem('30 mins', 30 * 60)
        self.ui.graph_visible_interval.addItem('1 hour', 60 * 60)
        self.ui.graph_visible_interval.addItem('6 hours', 6 * 60 * 60)
        self.ui.graph_visible_interval.addItem('12 hours', 12 * 60 * 60)
        self.ui.graph_visible_interval.addItem('1 day', 24 * 60 * 60)

    def _init_graph_view(self):
        self.plot = QtCharts.QChart()
        self.ui.graph.setChart(self.plot)

        self.axis_x = QtCharts.QDateTimeAxis()
        self.axis_x.setTickCount(10)
        self.axis_x.setFormat("hh:mm:ss")
        self.axis_x.setTitleText("Date")
        self.axis_x.setMax(QtCore.QDateTime.currentDateTime().addSecs(60))
        self.axis_x.setMin(QtCore.QDateTime.currentDateTime())

        self.axis_y = QtCharts.QValueAxis()
        self.axis_y.setTickCount(7)
        self.axis_y.setLabelFormat("%i")
        self.axis_y.setTitleText("Ping [ms]")
        self.axis_y.setMax(100)
        self.axis_y.setMin(0)

        self.plot.setAxisX(self.axis_x)
        self.plot.setAxisY(self.axis_y)

        self.ui.graph.setChart(self.plot)

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

    def _on_cur_server_changed(self, idx: int):
        recent_servers = self._get_recent_servers_from_combo()

        # move the currently chosen dir to the top
        cur_server = self.ui.recent_servers.itemText(idx)
        recent_servers.remove(cur_server)
        recent_servers.insert(0, cur_server)

        # to avoid infinite slot calls
        self.ui.recent_servers.currentIndexChanged.disconnect()

        self.ui.recent_servers.clear()
        for d in recent_servers:
            self.ui.recent_servers.addItem(d)

        self.ui.recent_servers.setCurrentIndex(0)

        # connect it back
        self.ui.recent_servers.currentIndexChanged.connect(self._on_cur_server_changed)

        # update settings
        settings.set_settings_list_value(SettingsKey.RECENT_SERVERS, self._get_recent_servers_from_combo())

    def _get_recent_servers_from_combo(self) -> List[str]:
        recent_dirs = list()
        for i in range(0, self.ui.recent_servers.count()):
            recent_dirs.append(self.ui.recent_servers.itemText(i))

        return recent_dirs

    def _update_start_stop_status(self):
        filled_elem_count = list(filter(lambda elem: len(elem.text()) > 0, elems))
        self.ui.start_stop.setEnabled(len(filled_elem_count) == len(elems))

    @Slot()
    def _start_ping(self):
        self._cancel_ping()

        logger.info('Start collecting statistics...')

        self._ping_stats.reset()

        self.series = QtCharts.QSplineSeries()
        # self.series.setName("Ping")
        self.plot.addSeries(self.series)
        self.series.setName(self.ui.recent_servers.currentText())

        self.plot.setAxisX(self.axis_x, self.series)
        self.plot.setAxisY(self.axis_y, self.series)

        self._set_all_controls_enabled(False)

        self.ui.start_stop.setText('Stop')
        self.ui.start_stop.clicked.disconnect()
        self.ui.start_stop.clicked.connect(self._cancel_ping)

        self._proc_mon = ProcessMonitor('ping', [self.ui.recent_servers.currentText()])
        self._proc_mon.start()

        self._timer = QTimer()
        self._timer.timeout.connect(self._update_cur_stats)
        self._timer.start(1000)

        # at the end
        self._started_time = datetime.datetime.now()
        self.started.emit()

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

        logger.info(f"Pinging {'done' if done else 'stopped'}")

    def _is_pinging(self) -> bool:
        return self._proc_mon is not None

    def _set_all_controls_enabled(self, enabled: bool = True):
        [elem.setEnabled(enabled) for elem in [
            self.ui.recent_servers
        ]]

    @Slot()
    def _update_cur_stats(self):
        # self.ui.stats_status.setText(f'<p style="color:green;">Statistics Ready (gen. {gen_datetime_str})</p')
        # cli_ret_code = self._proc_mon.is_cli_done()
        lines = self._proc_mon.lines if self._proc_mon else []
        print(lines)
        for line in lines:
            cur_ping = ping_output_parser.parse_line(line)
            print(cur_ping)
            if cur_ping is not None:
                self._ping_stats.add(cur_ping)
                self._add_ping_to_graph(cur_ping)

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
                duration_str += f'{days} d '
            if hours > 0:
                duration_str += f'{hours:02} h '
            if mins > 0:
                duration_str += f'{mins:02} m '
            duration_str += f'{secs:02} s'

            self.ui.duration.setText(duration_str)
        else:
            self.ui.start_time.setText('not started')
            self.ui.duration.setText('not started')

        self.ui.avg_ping.setText(f'{self._ping_stats.avg:.02f}')
        self.ui.min_ping.setText(str(self._ping_stats.min))
        self.ui.max_ping.setText(str(self._ping_stats.max))

    def _add_ping_to_graph(self, ping_value: int):
        cur_time = QtCore.QDateTime.currentDateTime()
        self.series.append(cur_time.toMSecsSinceEpoch(), ping_value)

        x_min, x_max = min(cur_time, cur_time.addSecs(-1 * self.ui.graph_visible_interval.currentData())), cur_time
        y_min, y_max = min(ping_value, self.axis_y.min()), max(ping_value, self.axis_y.max())

        self.axis_x.setRange(x_min, x_max)
        self.axis_y.setRange(y_min, y_max)

    @Slot()
    def _change_graph_visible_interval(self):
        right_value = self.axis_x.max()
        x_min, x_max = right_value.addSecs(-1 * self.ui.graph_visible_interval.currentData()), self.axis_x.max()
        self.axis_x.setRange(x_min, x_max)
