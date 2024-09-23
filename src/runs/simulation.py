import os

commands = []
# run gazebo


def run_commands():

    # commands = ["dependencies/PX4-Autopilot/Tools/simulation/gazebo-classic/sitl_multiple_run.sh -n 6 -m iris",
    #             "python3 src/mavsdk_server_shell.py udp://:14541 -p 50060",
    #             "python3 src/mavsdk_server_shell.py udp://:14542 -p 50061",
    #             "python3 src/mavsdk_server_shell.py udp://:14543 -p 50062",
    #             "python3 src/mavsdk_server_shell.py udp://:14544 -p 50063",
    #             "python3 src/mavsdk_server_shell.py udp://:14545 -p 50064",
    #             "python3 src/mavsdk_server_shell.py udp://:14546 -p 50065",
    #             "dependencies/QGroundControl.AppImage",
    #             "python3 src/main.py"]

    commands = [
        "dependencies/PX4-Autopilot/Tools/simulation/gazebo-classic/sitl_multiple_run.sh -n 6 -m iris",
        "python3 src/mavsdk_server_shell.py udp://:14541 -p 50060",
        "python3 src/mavsdk_server_shell.py udp://:14542 -p 50061",
        "python3 src/mavsdk_server_shell.py udp://:14543 -p 50062",
        "python3 src/mavsdk_server_shell.py udp://:14544 -p 50063",
        "python3 src/mavsdk_server_shell.py udp://:14545 -p 50064",
        "python3 src/mavsdk_server_shell.py udp://:14546 -p 50065",
        "watch -n 0.5 netstat -lunp",
        "python3 src/main.py"]

    for command in commands:
        try:
            os.system(
                f"gnome-terminal -- /bin/bash -c  'sleep 1; {command}; exec /bin/bash' &")
        except Exception as e:
            print(f"Exception {repr(e)} was thrown at command {command}")


if __name__ == "__main__":
    run_commands()
