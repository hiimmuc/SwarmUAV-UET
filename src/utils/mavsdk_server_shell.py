#!/usr/bin/env python3
# filepath: workspace/src/utils/mavsdk_server_shell.py
"""
MAVSDK Shell Interface

This module provides a command-line shell interface to a drone via MAVSDK.
It allows connecting to a drone system, running health checks, and sending
shell commands to the drone's onboard computer.

Example usage:
    $ python mavsdk_server_shell.py udp://:14540 -p 50060 -i 1 -c
"""

import argparse
import asyncio
import sys
from typing import Optional

from mavsdk import System

from utils.logger import get_logger

# Initialize logger
logger = get_logger(
    name="mavsdk_shell", 
    console_level="info",
    file_level="debug",
    log_file="mavsdk_shell.log"
)


async def run(
    system_address: str, 
    port: str, 
    id: int, 
    health_check: bool = False,
    timeout: int = 30
) -> None:
    """
    Connect to a drone and set up shell communication.
    
    Args:
        system_address: The address of the drone system in URL format
            (e.g., udp://:14540, serial:///dev/ttyUSB0:57600)
        port: The MAVSDK server port for communicating with the drone
        id: The identifier for the drone system
        health_check: If True, verify the drone has a global position estimate
        timeout: Maximum time in seconds to wait for connection
        
    Returns:
        None
        
    Raises:
        TimeoutError: If connection or health check times out
    """
    # Initialize drone connection
    drone = System(port=port)
    
    logger.info(f"Connecting to drone {id} at {system_address}...")
    connection_task = asyncio.create_task(
        establish_connection(drone, system_address, id, timeout)
    )
    
    # Start shell observer in parallel
    shell_task = asyncio.create_task(observe_shell(drone))
    
    # Wait for connection
    await connection_task
    
    # If requested, perform health check
    if health_check:
        logger.info(f"Performing health check for drone {id}...")
        await verify_health(drone, id, timeout)
    
    # Set up stdin handling for interactive shell
    asyncio.get_event_loop().add_reader(sys.stdin, got_stdin_data, drone)
    print("nsh> ", end="", flush=True)


async def establish_connection(
    drone: System, 
    system_address: str, 
    id: int, 
    timeout: int
) -> None:
    """
    Establish connection with the drone system.
    
    Args:
        drone: MAVSDK System object
        system_address: Connection URL string
        id: Drone identifier
        timeout: Maximum time in seconds to wait for connection
        
    Raises:
        TimeoutError: If connection times out
    """
    # Start connection process
    await drone.connect(system_address=system_address)
    
    # Create connection task with timeout
    try:
        async with asyncio.timeout(timeout):
            async for state in drone.core.connection_state():
                if state.is_connected:
                    logger.info(f"Connected to drone {id} successfully")
                    return
    except asyncio.TimeoutError:
        logger.error(f"Timeout connecting to drone {id}")
        raise TimeoutError(f"Could not connect to drone {id} at {system_address}")


async def verify_health(drone: System, id: int, timeout: int) -> None:
    """
    Verify the drone has a valid global position estimate.
    
    Args:
        drone: MAVSDK System object
        id: Drone identifier
        timeout: Maximum time in seconds to wait for health check
        
    Raises:
        TimeoutError: If health check times out
    """
    logger.info(f"Waiting for drone {id} to have a global position estimate...")
    
    try:
        async with asyncio.timeout(timeout):
            async for health in drone.telemetry.health():
                if health.is_global_position_ok and health.is_home_position_ok:
                    logger.info(f"Global position estimate OK for drone {id}")
                    return
    except asyncio.TimeoutError:
        logger.error(f"Timeout waiting for global position from drone {id}")
        raise TimeoutError(f"Drone {id} did not provide global position within {timeout} seconds")


async def observe_shell(drone: System) -> None:
    """
    Continuously monitor and display shell output from the drone.
    
    Args:
        drone: MAVSDK System object
    """
    try:
        async for output in drone.shell.receive():
            # Print received shell output, ensuring prompt remains intact
            if output.strip():  # Only print non-empty lines
                print(f"\n{output}", end="", flush=True)
                print("nsh> ", end="", flush=True)
    except Exception as e:
        logger.error(f"Shell receive error: {e}")
        print(f"\nError receiving shell data: {e}")
        print("nsh> ", end="", flush=True)


def got_stdin_data(drone: System) -> None:
    """
    Handle user input from stdin.
    
    This function is called when data is available on stdin.
    It reads a line from stdin and sends it to the drone's shell.
    
    Args:
        drone: MAVSDK System object
    """
    command = sys.stdin.readline()
    asyncio.ensure_future(send_command(drone, command))


async def send_command(drone: System, command: str) -> None:
    """
    Send a command to the drone's shell.
    
    Args:
        drone: MAVSDK System object
        command: Command string to send
    """
    try:
        await drone.shell.send(command)
    except Exception as e:
        logger.error(f"Failed to send command: {e}")
        print(f"\nError sending command: {e}")
        print("nsh> ", end="", flush=True)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Parsed argument namespace
    """
    parser = argparse.ArgumentParser(
        description="MAVSDK interactive shell interface",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "system_address",
        type=str,
        nargs="?",
        default="udp://:14540",
        help="""The address of the remote system. Supported URL formats:
                - Serial: serial:///path/to/serial/dev[:baudrate]
                - UDP: udp://[bind_host][:bind_port]
                - TCP: tcp://[server_host][:server_port]"""
    )
    
    parser.add_argument(
        "-p", "--port",
        type=str,
        default="50060",
        help="MAVSDK server port (default: 50060)"
    )
    
    parser.add_argument(
        "-i", "--id",
        type=int,
        default=0,
        help="Drone identifier (default: 0)"
    )
    
    parser.add_argument(
        "-c", "--check-health",
        action="store_true",
        help="Perform health check to verify global position"
    )
    
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=30,
        help="Connection timeout in seconds (default: 30)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser.parse_args()


async def main() -> None:
    """Main entry point for the application."""
    args = parse_arguments()
    
    # Set logging level based on verbosity
    if args.verbose:
        logger.set_level("debug")
    
    try:
        await run(
            system_address=args.system_address,
            port=args.port,
            id=args.id,
            health_check=args.check_health,
            timeout=args.timeout
        )
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        sys.exit(1)


async def cleanup() -> None:
    """Clean up resources before exiting."""
    # Clean up file handles
    try:
        # Remove stdin reader if it was added
        loop = asyncio.get_event_loop()
        try:
            loop.remove_reader(sys.stdin)
        except Exception:
            pass  # Reader might not be registered
    except Exception as e:
        logger.warning(f"Error during cleanup: {e}")


if __name__ == "__main__":
    try:
        # Create and run main task
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program terminated by user")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
    finally:
        # Ensure proper cleanup
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(cleanup())
            
            # Cancel pending tasks
            pending = asyncio.all_tasks(loop=loop)
            for task in pending:
                task.cancel()
                
            if pending:
                loop.run_until_complete(asyncio.wait(pending, timeout=5))
        except Exception as e:
            logger.error(f"Error during final cleanup: {e}")
        finally:
            sys.exit(0)