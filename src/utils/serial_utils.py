import asyncio

import serial
import serial.tools.list_ports
from mavsdk import rtk

# cspell:ignore serials rtcm mavsdk


def find_base_station_port(baud_rate=115200, timeout=1):
    # List all available serial ports
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            # Attempt to open each port and check if it returns RTCM-like data
            with serial.Serial(port.device, baud_rate, timeout=timeout) as ser:
                # Read a small amount of data to see if it's likely RTCM (starting with 0xD3)
                data = ser.read(100)
                if data and data.startswith(b"\xd3"):  # RTCM messages typically start with 0xD3
                    print(f"H-RTK F9P base station found on port: {port.device}")
                    return port.device
        except Exception as e:
            # Ignore ports that can't be opened or don't return valid data
            print(f"Skipping port {port.device}: {e}")
    raise Exception("No H-RTK F9P base station found.")


async def send_rtcm(drone, base_station_port):
    # Open the detected base station port
    with serial.Serial(base_station_port, 115200, timeout=1) as ser:
        while True:
            try:
                # Read RTCM data from the serial port
                if ser.in_waiting > 0:
                    rtcm_correction_data = ser.read(1024)  # Read up to 1024 bytes of RTCM data
                    if rtcm_correction_data:
                        # Send the RTCM data to the drone
                        await drone.rtk.send_rtcm_data(rtk.RtcmData(rtcm_correction_data))
            except Exception as e:
                print(f"Exception while sending RTCM data: {e}")

            await asyncio.sleep(1)
