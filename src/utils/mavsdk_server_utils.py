import os
import shlex
import signal
import subprocess
from pathlib import Path

import psutil

from config.interface_config import ROOT_DIR

# remember to assign subprocess to a variable
CMD = f"{ROOT_DIR}/dependencies/MAVSDK-Python/mavsdk/bin/mavsdk_server"


def kills(pid):
    """Kills all process"""
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()


def get_pids_by_script_name(script):
    PIDs = []
    for proc in psutil.process_iter():

        try:
            cmdline = proc.cmdline()
            pid = proc.pid
        except psutil.NoSuchProcess:
            continue

        if cmdline == script:
            PIDs.append(pid)

    return PIDs


class Server:
    def __init__(self, id, proto, server_host, port, bind_port):

        if Path(CMD).exists():
            self.command = f"{CMD} {proto}://{server_host}:{bind_port} -p {port}"
        else:
            self.command = f"python3 src/mavsdk_server_shell.py {proto}://{server_host}:{bind_port} -p {port} -i {id}"

        self.init_msg = f"[INFO] Starting MAVSDK server {id} with {proto}://{server_host}:{bind_port} -p {port}"
        self.shell = f"gnome-terminal -- /bin/bash -c  'echo {self.init_msg}; sleep 1; {self.command}; exec /bin/bash' &"

        self.process = None

    def start(self):
        try:
            self.process = subprocess.Popen(
                self.shell,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
        except Exception as e:
            print(f"Exception {repr(e)} was thrown at command {self.command}")

    def stop(self):
        # shell_pid = get_pids_by_script_name(shlex.split(self.shell)[2:-1])[0]
        # kills(shell_pid)
        pass
