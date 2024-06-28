import os

def run_commands():
    # Danh sách các lệnh cần chạy
    commands = [
        ".local/lib/python3.10/site-packages/mavsdk/bin/mavsdk_server serial:///dev/ttyUSB0:57600 -p 50060",
        ".local/lib/python3.10/site-packages/mavsdk/bin/mavsdk_server serial:///dev/ttyUSB1:57600 -p 50061",
        ".local/lib/python3.10/site-packages/mavsdk/bin/mavsdk_server serial:///dev/ttyUSB2:57600 -p 50062",
        #".local/lib/python3.10/site-packages/mavsdk/bin/mavsdk_server serial:///dev/ttyUSB3:57600 -p 50063",
        #".local/lib/python3.10/site-packages/mavsdk/bin/mavsdk_server serial:///dev/ttyUSB4:57600 -p 50064",
        #".local/lib/python3.10/site-packages/mavsdk/bin/mavsdk_server serial:///dev/ttyUSB5:57600 -p 50065",
        "python3 new7/main.py"
    ]

    # Mở 7 terminal độc lập và chạy từng lệnh trên mỗi terminal
    for command in commands:
        os.system(f"gnome-terminal -- /bin/bash -c '{command}; exec /bin/bash' &")

if __name__ == "__main__":
    run_commands()
