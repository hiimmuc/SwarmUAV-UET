#!/usr/bin/env python3

import asyncio
import sys
import argparse

from mavsdk import System


async def run(system_address, port):
    drone = System(port=port)
    await drone.connect(system_address=system_address)

    # status_text_task = asyncio.ensure_future(print_status_text(drone))
    asyncio.ensure_future(observe_shell(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    asyncio.get_event_loop().add_reader(sys.stdin, got_stdin_data, drone)
    print("nsh> ", end='', flush=True)

    # entries = await get_entries(drone)
    # for entry in entries:
    #     await download_log(drone, entry)

    # status_text_task.cancel()


async def download_log(drone, entry):
    date_without_colon = entry.date.replace(":", "-")
    filename = f"./log-{date_without_colon}.ulog"
    print(f"Downloading: log {entry.id} from {entry.date} to {filename}")
    previous_progress = -1
    async for progress in drone.log_files.download_log_file(entry, filename):
        new_progress = round(progress.progress*100)
        if new_progress != previous_progress:
            sys.stdout.write(f"\r{new_progress} %")
            sys.stdout.flush()
            previous_progress = new_progress
    print()


async def get_entries(drone):
    entries = await drone.log_files.get_entries()
    for entry in entries:
        print(f"Log {entry.id} from {entry.date}")
    return entries


async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return


async def observe_shell(drone):
    async for output in drone.shell.receive():
        print(f"\n{output} ", end='', flush=True)


def got_stdin_data(drone):
    asyncio.ensure_future(send(drone, sys.stdin.readline()))


async def send(drone, command):
    await drone.shell.send(command)

parser = argparse.ArgumentParser(description="MAV SDK server")
if __name__ == "__main__":
    parser.add_argument('system_address', metavar='A', type=str, default='udp://:14540',
                        help='The address of the remote system. If None, it will default to udp://:14540. Supported URL formats:\n\
                        - Serial: serial:///path/to/serial/dev[:baudrate]\n\
                        - UDP: udp://[bind_host][:bind_port]\n\
                        - TCP: tcp://[server_host][:server_port]')
    parser.add_argument('-p', '--port', type=str, default='50060')

    args = parser.parse_args()

    asyncio.ensure_future(
        run(system_address=args.system_address, port=args.port))

    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
