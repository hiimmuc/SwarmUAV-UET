import os
import subprocess

import psutil

# remember to assign subprocess to a variable


def kills(pid):
    """Kills all process"""
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()


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
            s = subprocess.check_call(
                self.shell,
                shell=True,
            )
            if s != 0:
                print(f"Command {self.command} failed with status {s}")
        except Exception as e:
            print(f"Exception {repr(e)} was thrown at command {self.command}")

    def restart(self):
        try:
            s = subprocess.run(
                self.shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            if s != 0:
                print(f"Command {self.command} failed with status {s}")
        except Exception as e:
            print(f"Exception {repr(e)} was thrown at command {self.command}")

    def stop(self):
        kills(self.process.pid)
