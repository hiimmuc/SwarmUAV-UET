#!/usr/bin/env python3

import argparse
import asyncio
import subprocess
import sys
from pathlib import Path

from mavsdk import System

from config.interface_config import *

# cspell: ignore mavsdk baudrate


async def run(system_address, port, id, health_check=False):
    drone = System(port=port)
    await drone.connect(system_address=system_address)

    asyncio.ensure_future(observe_shell(drone))

    print(f"Waiting for drone {id} to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone {id} !")
            break

    if health_check:
        print(f"Waiting for drone {id} to have a global position estimate...")
        async for health in drone.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                print("-- Global position estimate OK")
                break

    asyncio.get_event_loop().add_reader(sys.stdin, got_stdin_data, drone)
    print("nsh> ", end="", flush=True)


async def observe_shell(drone):
    async for output in drone.shell.receive():
        print(f"\n{output} ", end="", flush=True)


def got_stdin_data(drone):
    asyncio.ensure_future(send(drone, sys.stdin.readline()))


async def send(drone, command):
    await drone.shell.send(command)


async def receive(drone):
    async for output in drone.shell.receive():
        print(f"\n{output} ", end="", flush=True)


parser = argparse.ArgumentParser(description="MAV SDK server")
if __name__ == "__main__":
    parser.add_argument(
        "system_address",
        metavar="A",
        type=str,
        default="udp://:14540",
        help="The address of the remote system. If None, it will default to udp://:14540. Supported URL formats:\n\
                        - Serial: serial:///path/to/serial/dev[:baudrate]\n\
                        - UDP: udp://[bind_host][:bind_port]\n\
                        - TCP: tcp://[server_host][:server_port]",
    )
    parser.add_argument("-p", "--port", type=str, default="50060")
    parser.add_argument("-i", "--id", type=int, default=0)

    args = parser.parse_args()

    asyncio.ensure_future(run(system_address=args.system_address, port=args.port, id=args.id))
    # run_server_cmd(system_address=args.system_address, port=args.port, id=args.id)

    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
