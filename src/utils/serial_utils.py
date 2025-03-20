#!/usr/bin/env python3
# filepath: workspace/src/utils/serial_utils.py
"""
Serial Utilities for RTK Base Station

This module provides utilities for working with RTK base stations over serial connections,
including detecting RTK base stations and forwarding RTCM correction data to drones.
"""

import asyncio
from typing import List, Optional, Tuple

import serial
import serial.tools.list_ports
from mavsdk import System, rtk

from utils.logger import get_logger

# Initialize logger
logger = get_logger(
    name="serial_utils",
    console_level="info",
    file_level="debug",
    log_file="rtk_serial.log"
)

# RTK Constants
DEFAULT_BAUD_RATE = 115200
DEFAULT_TIMEOUT = 1
RTCM_HEADER = b"\xd3"  # RTCM messages typically start with 0xD3
MAX_RTCM_BUFFER = 1024


def list_available_ports() -> List[Tuple[str, str, str]]:
    """
    List all available serial ports on the system.
    
    Returns:
        List of tuples containing (port_name, description, hardware_id)
    """
    ports = serial.tools.list_ports.comports()
    return [(port.device, port.description, port.hwid) for port in ports]


def find_base_station_port(
    baud_rate: int = DEFAULT_BAUD_RATE, 
    timeout: float = DEFAULT_TIMEOUT,
    verbose: bool = False
) -> Optional[str]:
    """
    Find the serial port connected to an RTK base station.
    
    This function scans all available serial ports and checks for RTCM data
    to identify an RTK base station.
    
    Args:
        baud_rate: Baud rate for serial communication
        timeout: Timeout in seconds for serial read operations
        verbose: If True, print detailed information about all scanned ports
        
    Returns:
        Device path of the identified RTK base station, or None if not found
        
    Raises:
        serial.SerialException: If there's an error accessing a serial port
    """
    # List all available serial ports
    ports = serial.tools.list_ports.comports()
    if verbose:
        logger.info(f"Found {len(ports)} serial ports")
        
    for port in ports:
        try:
            # Attempt to open each port and check if it returns RTCM-like data
            if verbose:
                logger.info(f"Checking port: {port.device} ({port.description})")
                
            with serial.Serial(
                port=port.device, 
                baudrate=baud_rate, 
                timeout=timeout
            ) as ser:
                # Read a small amount of data to see if it's likely RTCM
                data = ser.read(100)
                
                if data and data.startswith(RTCM_HEADER):
                    logger.info(f"RTK base station found on port: {port.device}")
                    return port.device
                elif verbose and data:
                    logger.debug(f"Port {port.device} returned non-RTCM data")
                    
        except serial.SerialException as e:
            if verbose:
                logger.warning(f"Could not open port {port.device}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error with port {port.device}: {e}")
            
    logger.warning("No RTK base station found on any port")
    return None


async def send_rtcm(
    drone: System, 
    base_station_port: str,
    baud_rate: int = DEFAULT_BAUD_RATE,
    read_interval: float = 0.1,
    max_buffer_size: int = MAX_RTCM_BUFFER
) -> None:
    """
    Forward RTCM correction data from the RTK base station to the drone.
    
    This function continuously reads RTCM data from the specified serial port
    and forwards it to the drone's RTK module.
    
    Args:
        drone: MAVSDK System object for the target drone
        base_station_port: Serial port connected to the RTK base station
        baud_rate: Baud rate for serial communication
        read_interval: Interval between serial port reads in seconds
        max_buffer_size: Maximum number of bytes to read at once
        
    Note:
        This function runs indefinitely and should be executed as a background task.
    """
    logger.info(f"Starting RTCM forwarding from {base_station_port} to drone")
    
    # Statistics counters
    packets_sent = 0
    bytes_sent = 0
    last_stats_time = asyncio.get_event_loop().time()
    
    try:
        # Open the detected base station port
        with serial.Serial(
            port=base_station_port, 
            baudrate=baud_rate, 
            timeout=DEFAULT_TIMEOUT
        ) as ser:
            logger.info(f"Connected to RTK base station on {base_station_port}")
            
            while True:
                try:
                    # Check if there's data available to read
                    if ser.in_waiting > 0:
                        # Read RTCM data from the serial port
                        rtcm_data = ser.read(max_buffer_size)
                        
                        if rtcm_data:
                            # Send the RTCM data to the drone
                            await drone.rtk.send_rtcm_data(rtk.RtcmData(rtcm_data))
                            
                            # Update statistics
                            packets_sent += 1
                            bytes_sent += len(rtcm_data)
                            
                            # Log statistics every 10 seconds
                            current_time = asyncio.get_event_loop().time()
                            if current_time - last_stats_time >= 10:
                                logger.info(
                                    f"RTCM forwarding stats: {packets_sent} packets, "
                                    f"{bytes_sent} bytes total"
                                )
                                last_stats_time = current_time
                                
                except serial.SerialException as e:
                    logger.error(f"Serial error: {e}")
                    # Try to recover by reopening the serial port
                    break
                except asyncio.CancelledError:
                    logger.info("RTCM forwarding task cancelled")
                    raise
                except Exception as e:
                    logger.error(f"Error sending RTCM data: {e}")
                
                # Short sleep to avoid busy-waiting
                await asyncio.sleep(read_interval)
                
    except serial.SerialException as e:
        logger.error(f"Failed to open RTK base station on {base_station_port}: {e}")
    finally:
        logger.info(f"RTCM forwarding stopped. Sent {packets_sent} packets, {bytes_sent} bytes total.")


async def setup_rtk_connection(drone: System) -> asyncio.Task:
    """
    Set up RTK connection for a drone.
    
    This function detects an RTK base station and starts forwarding RTCM data to the drone.
    
    Args:
        drone: MAVSDK System object for the target drone
        
    Returns:
        The async task handling the RTCM forwarding
        
    Raises:
        RuntimeError: If no RTK base station is found
    """
    # Find the RTK base station port
    base_station_port = find_base_station_port(verbose=True)
    
    if not base_station_port:
        raise RuntimeError("No RTK base station found. Cannot set up RTK corrections.")
    
    # Start the RTCM forwarding task
    logger.info(f"Starting RTCM forwarding from {base_station_port}")
    rtcm_task = asyncio.create_task(send_rtcm(drone, base_station_port))
    
    # Return the task so it can be cancelled if needed
    return rtcm_task


# Example usage
if __name__ == "__main__":
    import sys
    
    async def main():
        """Example of how to use the serial utilities."""
        # List available serial ports
        print("Available serial ports:")
        for port, desc, hwid in list_available_ports():
            print(f" - {port}: {desc} [{hwid}]")
        
        # Try to find an RTK base station
        print("\nSearching for RTK base station...")
        rtk_port = find_base_station_port(verbose=True)
        
        if not rtk_port:
            print("No RTK base station found. Exiting.")
            return 1
            
        print(f"RTK base station found on {rtk_port}")
        
        # Ask for drone connection details
        drone_address = input("\nEnter drone connection address (default: udp://:14540): ")
        if not drone_address:
            drone_address = "udp://:14540"
        
        # Connect to the drone
        print(f"Connecting to drone at {drone_address}...")
        drone = System()
        await drone.connect(system_address=drone_address)
        
        # Wait for the drone to connect
        print("Waiting for drone connection...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print("Drone connected!")
                break
        
        # Start RTCM forwarding
        print(f"Starting RTCM forwarding from {rtk_port} to drone...")
        rtcm_task = asyncio.create_task(send_rtcm(drone, rtk_port))
        
        # Keep the program running until interrupted
        try:
            print("Press Ctrl+C to stop RTCM forwarding")
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping RTCM forwarding...")
            rtcm_task.cancel()
            try:
                await rtcm_task
            except asyncio.CancelledError:
                pass
            print("RTCM forwarding stopped")
        
        return 0
    
    # Run the example
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    sys.exit(asyncio.run(main()))