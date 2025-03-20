#!/usr/bin/env python3
# filepath: /media/phgnam-d/920C22060C21E5C7/Personal/Workspace/UAV/workspace/src/utils/system_info.py
"""
System Information Utility

This module provides utilities for gathering and displaying detailed system information
including CPU, memory, disk, and network information.

The module can be run directly to print system information to the console,
or its functions can be imported and used in other modules.
"""

import platform
import re
import socket
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

import cpuinfo
import psutil


def format_bytes(bytes_value: int, suffix: str = "B") -> str:
    """
    Format bytes value to human-readable string with appropriate units.
    
    Args:
        bytes_value: Size in bytes
        suffix: Suffix to append to the unit (default: 'B' for Bytes)
        
    Returns:
        Formatted string (e.g., '1.20MB' or '1.17GB')
        
    Examples:
        >>> format_bytes(1253656)
        '1.20MB'
        >>> format_bytes(1253656678)
        '1.17GB'
    """
    if bytes_value < 0:
        return "0B"
        
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if bytes_value < factor:
            return f"{bytes_value:.2f}{unit}{suffix}"
        bytes_value /= factor
        
    return f"{bytes_value:.2f}Y{suffix}"


def get_system_info() -> Dict[str, Any]:
    """
    Get basic system information including OS, CPU, and network details.
    
    Returns:
        Dictionary containing system information
    """
    uname = platform.uname()
    
    # Get CPU information
    try:
        cpu_info = cpuinfo.get_cpu_info()
        cpu_brand = cpu_info.get('brand_raw', 'Unknown')
    except Exception:
        cpu_brand = 'Information unavailable'
    
    # Get IP and MAC address
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        ip_address = "Could not determine IP address"
        
    mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    
    return {
        "system": uname.system,
        "node_name": uname.node,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "processor": uname.processor,
        "cpu_brand": cpu_brand,
        "ip_address": ip_address,
        "mac_address": mac_address,
    }


def get_boot_time() -> Dict[str, Any]:
    """
    Get system boot time information.
    
    Returns:
        Dictionary containing boot time details
    """
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time_timestamp)
    
    return {
        "timestamp": boot_time_timestamp,
        "datetime": boot_time,
        "formatted": f"{boot_time.year}/{boot_time.month:02d}/{boot_time.day:02d} "
                     f"{boot_time.hour:02d}:{boot_time.minute:02d}:{boot_time.second:02d}"
    }


def get_cpu_info() -> Dict[str, Any]:
    """
    Get detailed CPU information including core count and frequencies.
    
    Returns:
        Dictionary containing CPU information
    """
    # Core counts
    physical_cores = psutil.cpu_count(logical=False)
    total_cores = psutil.cpu_count(logical=True)
    
    # CPU frequencies
    try:
        cpufreq = psutil.cpu_freq()
        max_freq = cpufreq.max if cpufreq else 0
        min_freq = cpufreq.min if cpufreq else 0
        current_freq = cpufreq.current if cpufreq else 0
    except AttributeError:
        max_freq = min_freq = current_freq = 0
    
    # CPU usage per core
    per_core_usage = psutil.cpu_percent(percpu=True, interval=0.1)
    total_usage = psutil.cpu_percent(interval=0.1)
    
    return {
        "physical_cores": physical_cores,
        "total_cores": total_cores,
        "max_frequency": max_freq,
        "min_frequency": min_freq,
        "current_frequency": current_freq,
        "per_core_usage": per_core_usage,
        "total_usage": total_usage
    }


def get_memory_info() -> Dict[str, Dict[str, Any]]:
    """
    Get memory information including RAM and swap usage.
    
    Returns:
        Dictionary containing memory information
    """
    # RAM information
    virtual_memory = psutil.virtual_memory()
    ram_info = {
        "total": virtual_memory.total,
        "available": virtual_memory.available,
        "used": virtual_memory.used,
        "percentage": virtual_memory.percent
    }
    
    # Swap information
    swap_memory = psutil.swap_memory()
    swap_info = {
        "total": swap_memory.total,
        "free": swap_memory.free,
        "used": swap_memory.used,
        "percentage": swap_memory.percent
    }
    
    return {
        "ram": ram_info,
        "swap": swap_info
    }


def get_disk_info() -> Dict[str, Any]:
    """
    Get disk information including partitions and I/O statistics.
    
    Returns:
        Dictionary containing disk information
    """
    # Gather partition information
    partitions_info = []
    for partition in psutil.disk_partitions():
        partition_info = {
            "device": partition.device,
            "mountpoint": partition.mountpoint,
            "fstype": partition.fstype
        }
        
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            partition_info.update({
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percentage": usage.percent
            })
        except (PermissionError, FileNotFoundError):
            # Some partitions may not be accessible
            partition_info.update({
                "error": "Access denied or not mounted"
            })
            
        partitions_info.append(partition_info)
    
    # I/O statistics
    try:
        disk_io = psutil.disk_io_counters()
        io_info = {
            "read_bytes": disk_io.read_bytes,
            "write_bytes": disk_io.write_bytes,
            "read_count": disk_io.read_count,
            "write_count": disk_io.write_count,
            "read_time": disk_io.read_time,
            "write_time": disk_io.write_time
        }
    except AttributeError:
        io_info = {"error": "Disk I/O statistics not available"}
    
    return {
        "partitions": partitions_info,
        "io_stats": io_info
    }


def get_network_info() -> Dict[str, Any]:
    """
    Get network information including interfaces and I/O statistics.
    
    Returns:
        Dictionary containing network information
    """
    # Network interfaces
    interfaces = {}
    for interface_name, addresses in psutil.net_if_addrs().items():
        interfaces[interface_name] = {
            "ipv4": [],
            "ipv6": [],
            "mac": []
        }
        
        for address in addresses:
            if str(address.family) == "AddressFamily.AF_INET":
                interfaces[interface_name]["ipv4"].append({
                    "address": address.address,
                    "netmask": address.netmask,
                    "broadcast": address.broadcast
                })
            elif str(address.family) == "AddressFamily.AF_INET6":
                interfaces[interface_name]["ipv6"].append({
                    "address": address.address,
                    "netmask": address.netmask,
                    "broadcast": address.broadcast
                })
            elif str(address.family) == "AddressFamily.AF_PACKET":
                interfaces[interface_name]["mac"].append({
                    "address": address.address,
                    "netmask": address.netmask,
                    "broadcast": address.broadcast
                })
    
    # Network I/O statistics
    try:
        net_io = psutil.net_io_counters()
        io_stats = {
            "bytes_sent": net_io.bytes_sent,
            "bytes_received": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_received": net_io.packets_recv,
            "errors_in": net_io.errin,
            "errors_out": net_io.errout,
            "dropped_in": net_io.dropin,
            "dropped_out": net_io.dropout
        }
    except AttributeError:
        io_stats = {"error": "Network I/O statistics not available"}
    
    # Per-interface statistics if available
    per_nic_stats = {}
    try:
        nic_stats = psutil.net_io_counters(pernic=True)
        for nic, stats in nic_stats.items():
            per_nic_stats[nic] = {
                "bytes_sent": stats.bytes_sent,
                "bytes_received": stats.bytes_recv,
                "packets_sent": stats.packets_sent,
                "packets_received": stats.packets_recv
            }
    except Exception:
        per_nic_stats = {"error": "Per-interface statistics not available"}
    
    return {
        "interfaces": interfaces,
        "io_stats": io_stats,
        "per_interface_stats": per_nic_stats
    }


def get_all_system_info() -> Dict[str, Any]:
    """
    Gather all system information in a single data structure.
    
    Returns:
        Dictionary containing all system information
    """
    return {
        "system": get_system_info(),
        "boot_time": get_boot_time(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
        "network": get_network_info()
    }


def print_system_info() -> None:
    """
    Print formatted system information to the console.
    
    This function displays all system information in a human-readable format,
    with appropriate formatting and section headers.
    """
    info = get_all_system_info()
    
    # System Information
    print("=" * 40, "System Information", "=" * 40)
    system = info["system"]
    print(f"System: {system['system']}")
    print(f"Node Name: {system['node_name']}")
    print(f"Release: {system['release']}")
    print(f"Version: {system['version']}")
    print(f"Machine: {system['machine']}")
    print(f"Processor: {system['processor']}")
    print(f"CPU Brand: {system['cpu_brand']}")
    print(f"IP Address: {system['ip_address']}")
    print(f"MAC Address: {system['mac_address']}")
    
    # Boot Time
    print("\n" + "=" * 40, "Boot Time", "=" * 40)
    print(f"Boot Time: {info['boot_time']['formatted']}")
    
    # CPU Information
    print("\n" + "=" * 40, "CPU Info", "=" * 40)
    cpu = info["cpu"]
    print(f"Physical Cores: {cpu['physical_cores']}")
    print(f"Total Cores: {cpu['total_cores']}")
    print(f"Max Frequency: {cpu['max_frequency']:.2f}MHz")
    print(f"Min Frequency: {cpu['min_frequency']:.2f}MHz")
    print(f"Current Frequency: {cpu['current_frequency']:.2f}MHz")
    
    print("\nCPU Usage Per Core:")
    for i, percentage in enumerate(cpu['per_core_usage']):
        print(f"Core {i}: {percentage:.1f}%")
    print(f"Total CPU Usage: {cpu['total_usage']:.1f}%")
    
    # Memory Information
    print("\n" + "=" * 40, "Memory Information", "=" * 40)
    ram = info["memory"]["ram"]
    print(f"Total: {format_bytes(ram['total'])}")
    print(f"Available: {format_bytes(ram['available'])}")
    print(f"Used: {format_bytes(ram['used'])}")
    print(f"Percentage: {ram['percentage']:.1f}%")
    
    print("\n" + "=" * 20, "SWAP", "=" * 20)
    swap = info["memory"]["swap"]
    print(f"Total: {format_bytes(swap['total'])}")
    print(f"Free: {format_bytes(swap['free'])}")
    print(f"Used: {format_bytes(swap['used'])}")
    print(f"Percentage: {swap['percentage']:.1f}%")
    
    # Disk Information
    print("\n" + "=" * 40, "Disk Information", "=" * 40)
    print("Partitions and Usage:")
    for partition in info["disk"]["partitions"]:
        print(f"\n=== Device: {partition['device']} ===")
        print(f"  Mountpoint: {partition['mountpoint']}")
        print(f"  File system type: {partition['fstype']}")
        
        if "error" in partition:
            print(f"  {partition['error']}")
        else:
            print(f"  Total Size: {format_bytes(partition['total'])}")
            print(f"  Used: {format_bytes(partition['used'])}")
            print(f"  Free: {format_bytes(partition['free'])}")
            print(f"  Percentage: {partition['percentage']:.1f}%")
    
    # I/O statistics
    io_stats = info["disk"]["io_stats"]
    if "error" in io_stats:
        print(f"\n{io_stats['error']}")
    else:
        print(f"\nTotal read: {format_bytes(io_stats['read_bytes'])}")
        print(f"Total write: {format_bytes(io_stats['write_bytes'])}")
        print(f"Read operations: {io_stats['read_count']}")
        print(f"Write operations: {io_stats['write_count']}")
    
    # Network Information
    print("\n" + "=" * 40, "Network Information", "=" * 40)
    interfaces = info["network"]["interfaces"]
    
    for interface_name, addresses in interfaces.items():
        print(f"\n=== Interface: {interface_name} ===")
        
        for ipv4 in addresses["ipv4"]:
            print(f"  IP Address: {ipv4['address']}")
            if ipv4['netmask']:
                print(f"  Netmask: {ipv4['netmask']}")
            if ipv4['broadcast']:
                print(f"  Broadcast IP: {ipv4['broadcast']}")
                
        for mac in addresses["mac"]:
            print(f"  MAC Address: {mac['address']}")
            if mac['netmask']:
                print(f"  Netmask: {mac['netmask']}")
            if mac['broadcast']:
                print(f"  Broadcast MAC: {mac['broadcast']}")
    
    # Network I/O
    io_stats = info["network"]["io_stats"]
    if "error" in io_stats:
        print(f"\n{io_stats['error']}")
    else:
        print(f"\nTotal Bytes Sent: {format_bytes(io_stats['bytes_sent'])}")
        print(f"Total Bytes Received: {format_bytes(io_stats['bytes_received'])}")
        print(f"Total Packets Sent: {io_stats['packets_sent']}")
        print(f"Total Packets Received: {io_stats['packets_received']}")


def generate_system_report(format_type: str = "text") -> Union[str, Dict[str, Any]]:
    """
    Generate a system report in the specified format.
    
    Args:
        format_type: Report format ('text', 'json', or 'dict')
        
    Returns:
        Report as string or dictionary
    """
    info = get_all_system_info()
    
    if format_type.lower() == "json":
        import json

        # Convert datetime to string
        info_copy = info.copy()
        info_copy["boot_time"]["datetime"] = str(info_copy["boot_time"]["datetime"])
        return json.dumps(info_copy, indent=2)
    
    elif format_type.lower() == "dict":
        return info
        
    else:  # Text format
        import io
        from contextlib import redirect_stdout
        
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            print_system_info()
            
        return buffer.getvalue()


if __name__ == "__main__":
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Display system information including CPU, memory, disk, and network details."
    )
    parser.add_argument(
        "--format", 
        choices=["text", "json"], 
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        help="Output file (default: print to console)"
    )
    
    args = parser.parse_args()
    
    # Generate the report
    report = generate_system_report(args.format)
    
    # Output the report
    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"System information saved to {args.output}")
    else:
        if args.format == "text":
            # For text format, print_system_info is more efficient
            print_system_info()
        else:
            print(report)