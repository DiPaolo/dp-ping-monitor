import queue
import subprocess
import threading
from typing import Optional, List

from dp_ping_monitor.config import config


def _start_cli(cli_name: str, params, stdout_file=None, stderr_file=None) -> subprocess.Popen[str]:
    """Launches CLI and returns immediately

    :param cli_name: name of the command
    :param params: command line parameters
    :param stdout_file: (optional) file to print stdout to
    :param stderr_file: (optional) file to print stderr to
    :return: process handler
    """

    full_cmdline = [cli_name] + params

    if config.is_debug:
        print(f"> {' '.join(full_cmdline)}")

    shell = False

    if stdout_file is None:
        stdout_file = subprocess.PIPE

    if stderr_file is None:
        stderr_file = subprocess.PIPE

    return subprocess.Popen(full_cmdline, shell=shell, stdout=stdout_file, stderr=stderr_file, universal_newlines=True)


class ProcessMonitor(threading.Thread):
    _proc: Optional[subprocess.Popen[str]] = None
    _cli_name: str = None
    _lines = queue.Queue()

    def __init__(self, cli_name: str, cli_params: List[str]):
        threading.Thread.__init__(self)

        self._cli_name = cli_name
        self._cli_params = cli_params

    def __del__(self):
        self.stop()

    def stop(self):
        if self._proc:
            self._proc.terminate()

            try:
                self._proc.wait(10)
            except:
                self._proc.kill()

            self._proc = None

    def run(self):
        try:
            self._proc = _start_cli(self._cli_name, self._cli_params)

            # self.execute_lock.acquire()
            while True:
                output = self._proc.stdout.readline()
                if output == '' and self._proc.poll() is not None:
                    break
                if output:
                    self._lines.put(output)
        except ValueError:
            pass

    @property
    def lines(self):
        out = list()
        while not self._lines.empty():
            out.append(self._lines.get())

        return out

    def is_cli_done(self) -> Optional[int]:
        return self._proc.poll() if self._proc else None
