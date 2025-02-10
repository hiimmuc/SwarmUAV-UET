import os
import subprocess

os.environ["PX4_HOME_LAT"] = "21.064862"  # export PX4_HOME_LAT=21.043493300234438
os.environ["PX4_HOME_LON"] = "105.792958"  # export PX4_HOME_LON=105.72807953895773

PROTO = "udp"
SERVER_HOST = ""
DEFAULT_PORT = 50060
DEFAULT_BIND_PORT = 14541

commands = []

# run gazebo
# cspell: ignore mavsdk mavlink routerd sitl lunp


def run_commands():

    commands = [
        "dependencies/PX4-Autopilot/Tools/simulation/gazebo-classic/sitl_multiple_run.sh -n 6 -m iris",
        # " mavlink-routerd -t 5761 /dev/ttyACM0:57600 -e 127.0.0.1:14541 -e 127.0.0.1:14551",
        # f"python3 src/mavsdk_server_shell.py {PROTO}://{SERVER_HOST}:{DEFAULT_BIND_PORT + 0} -p {DEFAULT_PORT + 0}",
        # f"python3 src/mavsdk_server_shell.py {PROTO}://{SERVER_HOST}:{DEFAULT_BIND_PORT + 1} -p {DEFAULT_PORT + 1}",
        # f"python3 src/mavsdk_server_shell.py {PROTO}://{SERVER_HOST}:{DEFAULT_BIND_PORT + 2} -p {DEFAULT_PORT + 2}",
        # f"python3 src/mavsdk_server_shell.py {PROTO}://{SERVER_HOST}:{DEFAULT_BIND_PORT + 3} -p {DEFAULT_PORT + 3}",
        # f"python3 src/mavsdk_server_shell.py {PROTO}://{SERVER_HOST}:{DEFAULT_BIND_PORT + 4} -p {DEFAULT_PORT + 4}",
        # f"python3 src/mavsdk_server_shell.py {PROTO}://{SERVER_HOST}:{DEFAULT_BIND_PORT + 5} -p {DEFAULT_PORT + 5}",
        "python3 src/app.py",
        # "python3 src/map/DG5.py",
        # "dependencies/QGroundControl.AppImage",
        "watch -n 0.5 netstat -lunp",
    ]

    for i, command in enumerate(commands[:]):
        try:
            s = subprocess.check_call(
                f"gnome-terminal -- /bin/bash -c  'sleep 1; {command}; exec /bin/bash' &",
                shell=True,
            )
            if s != 0:
                print(f"Command {command} failed with status {s}")
        except Exception as e:
            print(f"Exception {repr(e)} was thrown at command {command}")


if __name__ == "__main__":
    run_commands()
