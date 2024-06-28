#!/usr/bin/env python3

import asyncio
import sys
import argparse

from mavsdk import System


async def run(system_address, port):
    drone = System(port=port)
    await drone.connect(system_address=system_address)

    asyncio.ensure_future(observe_shell(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    asyncio.get_event_loop().add_reader(sys.stdin, got_stdin_data, drone)
    print("nsh> ", end='', flush=True)


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
