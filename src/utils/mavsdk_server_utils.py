import os
import shlex
import signal
import subprocess

import psutil

# remember to assign subprocess to a variable


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
        self.id = id
        self.proto = proto
        self.server_host = server_host
        self.port = port
        self.bind_port = bind_port
        self.command = f"python3 src/mavsdk_server_shell.py {proto}://{server_host}:{bind_port} -p {port} -i {id}"
        self.shell = f"gnome-terminal -- /bin/bash -c  'sleep 1; {self.command}; exec /bin/bash' &"

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
