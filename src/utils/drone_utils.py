import asyncio
import json
import math
import os
import time
from pathlib import Path

from geographiclib.geodesic import Geodesic
from mavsdk.gimbal import ControlMode, GimbalMode
from mavsdk.mission import MissionItem, MissionPlan
from mavsdk.offboard import (
    ActuatorControl,
    ActuatorControlGroup,
    Offboard,
    OffboardError,
)

# cSpell:ignore asyncio, asyncgen offboard mavsdk
# Path to the source directory
SRC_DIR = Path(__file__).resolve().parent.parent


def calculate_distance(lat1, lon1, lat2, lon2) -> float:
    """
    Calculate the great-circle distance between two points on Earth.
    
    Uses the Haversine formula to calculate the distance between two points
    specified by their latitude and longitude in decimal degrees.
    
    Args:
        lat1 (float): Latitude of the first point in decimal degrees
        lon1 (float): Longitude of the first point in decimal degrees
        lat2 (float): Latitude of the second point in decimal degrees
        lon2 (float): Longitude of the second point in decimal degrees
    
    Returns:
        float: The distance between the two points in meters
    """
    R = 6378000  # Earth's radius in meters
    
    # Convert latitude and longitude differences to radians
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    
    # Apply Haversine formula
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)
    ) * math.sin(d_lon / 2) * math.sin(d_lon / 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance


async def print_mission_progress(drone) -> None:
    """
    Monitor and print the mission progress of a UAV.
    
    Args:
        drone (dict): A dictionary containing the UAV system with an 'ID' key
    
    Note:
        This is an asynchronous generator function that should be run as a background task
    """
    async for mission_progress in drone["system"].mission.mission_progress():
        print(
            f"Mission UAV-{drone['ID']} progress: "
            f"{mission_progress.current}/{mission_progress.total}"
        )


# --------------------- PARAMETER MANAGEMENT FUNCTIONS ---------------------

async def uav_fn_export_params(drone, save_path) -> None:
    """
    Export UAV parameters to a file.
    
    Args:
        drone (dict): UAV system dictionary
        save_path (str): File path where parameters will be saved
    """
    if save_path is None:
        return

    try:
        param_plugin = drone["system"].param
        params = await param_plugin.get_all_params()

        # Extract parameter names and values
        int_params = [(p.name, p.value) for p in params.int_params]
        float_params = [(p.name, p.value) for p in params.float_params]
        custom_params = [(p.name, p.value) for p in params.custom_params]
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Write parameters to file
        with open(save_path, "w") as wf:
            for name, value in int_params + float_params + custom_params:
                wf.write(f"{name}\t{value}\n")
                
    except Exception as e:
        print(f"Error exporting parameters: {repr(e)}")


def uav_fn_import_params(load_path) -> dict:
    """
    Import UAV parameters from a file.
    
    Args:
        load_path (str): Path to the parameter file
    
    Returns:
        dict: Dictionary of parameter names and values, or None if load_path is None
        
    Note:
        Each line in the file should have: vehicle_id, component_id, name, value, type
        Lines starting with '#' are considered comments
    """
    if load_path is None:
        return None
        
    if not os.path.exists(load_path):
        print(f"Parameter file not found: {load_path}")
        return {}
        
    parameters = {}

    try:
        with open(load_path, "r") as rf:
            for line in rf.readlines():
                if line.startswith("#") or not line.strip():
                    continue
                    
                columns = line.strip().split("\t")
                if len(columns) < 3:
                    print(f"Invalid parameter line: {line.strip()}")
                    continue
                    
                # Format: vehicle_id, component_id, name, value, type
                name = columns[2] if len(columns) >= 3 else columns[0]
                value = columns[3] if len(columns) >= 4 else columns[1]
                parameters[name] = value
                
        return parameters
        
    except Exception as e:
        print(f"Error importing parameters: {repr(e)}")
        return {}


async def uav_fn_get_params(drone, list_params=None) -> dict:
    """
    Get parameters from a UAV.
    
    Args:
        drone (dict): UAV system dictionary
        list_params (list, optional): List of specific parameters to retrieve
                                     If None, all parameters are retrieved
    
    Returns:
        dict: Dictionary of parameter names and values
    """
    parameters = {}

    try:
        param_plugin = drone["system"].param
        params = await param_plugin.get_all_params()

        # Extract parameter names for lookup
        int_param_names = [p.name for p in params.int_params]
        float_param_names = [p.name for p in params.float_params]
        custom_param_names = [p.name for p in params.custom_params]

        if list_params is None:
            # Get all parameters
            int_param_values = [p.value for p in params.int_params]
            float_param_values = [p.value for p in params.float_params]
            custom_param_values = [p.value for p in params.custom_params]

            param_names = int_param_names + float_param_names + custom_param_names
            param_values = int_param_values + float_param_values + custom_param_values
            
        else:
            # Get only specified parameters
            param_names = list_params
            param_values = []
            
            for param_name in param_names:
                try:
                    if param_name in int_param_names:
                        param = await param_plugin.get_param_int(param_name)
                    elif param_name in float_param_names:
                        param = await param_plugin.get_param_float(param_name)
                    elif param_name in custom_param_names:
                        param = await param_plugin.get_param_custom(param_name)
                    else:
                        print(f"Parameter not found: {param_name}")
                        param = None
                        
                    param_values.append(param)
                    
                except Exception as e:
                    print(f"Error retrieving parameter {param_name}: {repr(e)}")
                    param_values.append(None)

        # Create parameter dictionary
        for i, name in enumerate(param_names):
            if i < len(param_values):
                parameters[name] = param_values[i]

        return parameters
        
    except Exception as e:
        print(f"Error getting parameters: {repr(e)}")
        return parameters


async def uav_fn_set_params(drone, parameters=None, param_file=None) -> None:
    """
    Set parameters on a UAV.
    
    Args:
        drone (dict): UAV system dictionary
        parameters (dict, optional): Dictionary of parameters to set
        param_file (str, optional): Path to a file containing parameters
                                   Used if parameters dict is not provided
                                   
    Note:
        Parameter types (int, float, custom) are automatically detected
    """
    if parameters is None and param_file is None:
        print("No parameters or parameter file provided")
        return

    try:
        param_plugin = drone["system"].param
        params = await param_plugin.get_all_params()

        # Extract parameter names and types
        int_param_names = [p.name for p in params.int_params]
        float_param_names = [p.name for p in params.float_params]
        custom_param_names = [p.name for p in params.custom_params]

        # Import parameters from file if needed
        if parameters is None and param_file is not None:
            parameters = uav_fn_import_params(param_file)
            if not parameters:
                print(f"No valid parameters found in {param_file}")
                return

        # Set each parameter according to its type
        for param_name, param_value in parameters.items():
            try:
                if param_name in int_param_names:
                    await param_plugin.set_param_int(param_name, int(param_value))
                    # print(f"Set integer parameter {param_name} = {param_value}")
                    
                elif param_name in float_param_names:
                    await param_plugin.set_param_float(param_name, float(param_value))
                    # print(f"Set float parameter {param_name} = {param_value}")
                    
                elif param_name in custom_param_names:
                    await param_plugin.set_param_custom(param_name, str(param_value))
                    # print(f"Set custom parameter {param_name} = {param_value}")
                    
                else:
                    print(f"Unknown parameter: {param_name}, skipping")
                    
            except Exception as e:
                print(f"Error setting parameter {param_name}: {repr(e)}")
                
    except Exception as e:
        print(f"Error setting parameters: {repr(e)}")


async def uav_fn_overwrite_params(drone, parameters) -> None:
    """
    Overwrite critical UAV flight parameters.
    
    Args:
        drone (dict): UAV system dictionary
        parameters (dict): Dictionary with keys:
            - "RTL_AFTER_MS": Return to launch after mission (bool)
            - "GND_SPEED_MAX": Maximum ground speed (float)
            - "MIS_TAKEOFF_ALT": Takeoff altitude (float)
            - "CURRENT_SPEED": Current speed (float)
    """
    try:
        # Set return to launch after mission
        await drone["system"].mission.set_return_to_launch_after_mission(
            parameters.get("RTL_AFTER_MS", False)
        )
        
        # Set maximum speed
        await drone["system"].action.set_maximum_speed(
            parameters.get("GND_SPEED_MAX", 5.0)
        )
        
        # Set takeoff altitude
        takeoff_alt = parameters.get("MIS_TAKEOFF_ALT", 10.0)
        await drone["system"].action.set_takeoff_altitude(takeoff_alt)
        
        # Set return to launch altitude (same as takeoff altitude)
        await drone["system"].action.set_return_to_launch_altitude(takeoff_alt)
        
        # Set current speed
        await drone["system"].action.set_current_speed(
            parameters.get("CURRENT_SPEED", 2.0)
        )
        
        # print(f"Overwritten critical parameters for UAV-{drone['ID']}")
        
    except Exception as e:
        print(f"Error overwriting parameters: {repr(e)}")


# --------------------- NAVIGATION FUNCTIONS ---------------------

async def uav_fn_goto_location(drone, latitude=None, longitude=None, altitude=None) -> None:
    """
    Command UAV to go to a specific GPS location.
    
    Args:
        drone (dict): UAV system dictionary
        latitude (float, optional): Target latitude in degrees
                                   If None, current latitude is used
        longitude (float, optional): Target longitude in degrees
                                    If None, current longitude is used
        altitude (float, optional): Target altitude in meters
                                  If None, current altitude is used
                                  
    Note:
        The function waits until the drone reaches the target location
        within a small tolerance before returning
    """
    target_lat, target_lon, target_alt = None, None, None
    
    try:
        # Get current position if any coordinate is not specified
        async for position in drone["system"].telemetry.position():
            target_lat = latitude if latitude is not None else position.latitude_deg
            target_lon = longitude if longitude is not None else position.longitude_deg
            target_alt = altitude if altitude is not None else position.absolute_altitude_m
            
            # Command the UAV to go to the location
            # print(f"UAV-{drone['ID']} going to: {target_lat}, {target_lon}, {target_alt}m")
            await drone["system"].action.goto_location(target_lat, target_lon, target_alt, 0)
            break
            
        # Wait for the UAV to reach the target location
        await _wait_for_location_reached(drone, target_lat, target_lon, target_alt)
            
    except Exception as e:
        print(f"Error in goto_location: {repr(e)}")


async def _wait_for_location_reached(drone, target_lat, target_lon, target_alt, 
                                    tolerance_deg=1e-5, tolerance_alt=0.1, timeout=10):
    """
    Wait for UAV to reach a target location within tolerance.
    
    Args:
        drone (dict): UAV system dictionary
        target_lat (float): Target latitude in degrees
        target_lon (float): Target longitude in degrees
        target_alt (float): Target altitude in meters
        tolerance_deg (float): Tolerance for latitude/longitude in degrees
        tolerance_alt (float): Tolerance for altitude in meters
        timeout (int): Maximum wait time in seconds
        
    Returns:
        bool: True if target reached, False if timeout
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        async for position in drone["system"].telemetry.position():
            current_lat = position.latitude_deg
            current_lon = position.longitude_deg
            current_alt = position.absolute_altitude_m             
        
            lat_reached = abs(current_lat - target_lat) < tolerance_deg
            lon_reached = abs(current_lon - target_lon) < tolerance_deg
            alt_reached = abs(current_alt - target_alt) < tolerance_alt
            
            if lat_reached and lon_reached and alt_reached:
                print(f"UAV-{drone['ID']} at {[current_lat, current_lon, current_alt]} reached target location at {[target_lat, target_lon, target_alt]}")
                return True
                
            # Continue waiting if not reached
            await asyncio.sleep(0.5)
            break
            
    print(f"UAV-{drone['ID']} timeout reaching location")
    return False


async def uav_fn_goto_distance(drone, distance, direction) -> None:
    """
    Move UAV a specified distance in a given direction.
    
    Args:
        drone (dict): UAV system dictionary
        distance (float): Distance to move in meters
        direction (str): Direction to move ('forward', 'backward', 'left', 'right', 'up', 'down')
        
    Raises:
        ValueError: If the direction is invalid
    """
    r_earth = 6378137  # Earth radius in meters
    
    try:
        # Get current position
        async for position in drone["system"].telemetry.position():
            initial_lat = position.latitude_deg
            initial_lon = position.longitude_deg
            initial_alt = position.absolute_altitude_m
            
            # Calculate new position based on direction
            if direction == "forward":
                lat = initial_lat + (distance / r_earth) * (180 / math.pi)
                lon = initial_lon
                alt = initial_alt
                
            elif direction == "backward":
                lat = initial_lat - (distance / r_earth) * (180 / math.pi)
                lon = initial_lon
                alt = initial_alt
                
            elif direction == "left":
                lat = initial_lat
                lon = initial_lon - (distance / (r_earth * math.cos(math.pi * initial_lat / 180))) * (180 / math.pi)
                alt = initial_alt
                
            elif direction == "right":
                lat = initial_lat
                lon = initial_lon + (distance / (r_earth * math.cos(math.pi * initial_lat / 180))) * (180 / math.pi)
                alt = initial_alt
                
            elif direction == "up":
                lat = initial_lat
                lon = initial_lon
                alt = initial_alt + distance
                
            elif direction == "down":
                lat = initial_lat
                lon = initial_lon
                alt = initial_alt - distance
                
            else:
                raise ValueError(f"Invalid direction: {direction}")
                
            # Move to the new position
            # print(f"UAV-{drone['ID']} moving {distance}m {direction}")
            await uav_fn_goto_location(drone, lat, lon, alt)
            break
            
    except Exception as e:
        print(f"Error in goto_distance: {repr(e)}")


# --------------------- CONTROL FUNCTIONS ---------------------

async def uav_fn_offboard_set_actuator(drone, group, controls) -> None:
    """
    Control UAV actuators using offboard mode.
    
    Args:
        drone (dict): UAV system dictionary
        group (int): Actuator control group (0 or 1)
        controls (list): List of 8 control values for the actuator channels
        
    Raises:
        OffboardError: If starting or stopping offboard mode fails
        
    Note:
        This is a low-level function that provides direct control over actuators.
        Use with caution as improper use may cause unexpected behavior.
    """
    nan = float("nan")
    offsets1 = [nan] * 8  # 8 control channels for group 0
    offsets2 = [nan] * 8  # 8 control channels for group 1
    
    try:
        # Arm the UAV
        await drone["system"].action.arm()
        
        # Initialize actuator control with neutral values
        await drone["system"].offboard.set_actuator_control(
            ActuatorControl([ActuatorControlGroup(offsets1), ActuatorControlGroup(offsets2)])
        )
        
        # Start offboard mode
        print(f"UAV-{drone['ID']} starting offboard mode")
        await drone["system"].offboard.start()
        
        # Apply the specified controls to the appropriate group
        if group == 0:
            await drone["system"].offboard.set_actuator_control(
                ActuatorControl([ActuatorControlGroup(controls), ActuatorControlGroup(offsets2)])
            )
        elif group == 1:
            await drone["system"].offboard.set_actuator_control(
                ActuatorControl([ActuatorControlGroup(offsets1), ActuatorControlGroup(controls)])
            )
        else:
            print(f"Invalid actuator group: {group}, must be 0 or 1")
            
        # Allow time for controls to take effect
        await asyncio.sleep(2)
        
        # Stop offboard mode
        print(f"UAV-{drone['ID']} stopping offboard mode")
        await drone["system"].offboard.stop()
        
    except OffboardError as error:
        print(f"Offboard mode error: {error._result.result}")
        print("Disarming UAV")
        await drone["system"].action.disarm()
        
    except Exception as e:
        print(f"Error in offboard_set_actuator: {repr(e)}")
        try:
            # Attempt to stop offboard mode in case of error
            await drone["system"].offboard.stop()
        except:
            pass


async def uav_fn_control_gimbal(drone, control_value={"pitch": 0, "yaw": 0}) -> None:
    """
    Control the UAV gimbal.
    
    Args:
        drone (dict): UAV system dictionary
        control_value (dict): Dictionary with pitch and yaw values in degrees
                            pitch: 0 = horizontal, -90 = down
                            yaw: 0 = forward, values in degrees
    """
    try:
        # Take control of the gimbal
        await drone["system"].gimbal.take_control(
            control_mode=ControlMode.PRIMARY
        )
        
        # Set gimbal mode to YAW_FOLLOW (yaw follows aircraft heading)
        await drone["system"].gimbal.set_mode(
            GimbalMode.YAW_FOLLOW
        )
        
        # Set pitch and yaw angles
        pitch = control_value.get("pitch", 0)
        yaw = control_value.get("yaw", 0)
        
        print(f"UAV-{drone['ID']} setting gimbal to pitch: {pitch}°, yaw: {yaw}°")
        await drone["system"].gimbal.set_pitch_and_yaw(pitch, yaw)
        
        # Allow time for gimbal to move
        await asyncio.sleep(2)
        
        # Release control of the gimbal
        await drone["system"].gimbal.release_control()
        
    except Exception as e:
        print(f"Error controlling gimbal: {repr(e)}")
        # Try to release control in case of error
        try:
            await drone["system"].gimbal.release_control()
        except:
            pass


# --------------------- MISSION FUNCTIONS ---------------------

async def uav_fn_is_on_mission(drone) -> bool:
    """
    Check if UAV is currently executing a mission.
    
    Args:
        drone (dict): UAV system dictionary
        
    Returns:
        bool: True if on mission, False otherwise
    """
    try:
        async for mission_progress in drone["system"].mission.mission_progress():
            return mission_progress.current < mission_progress.total
    except Exception as e:
        print(f"Error checking mission status: {repr(e)}")
        return False


async def observe_is_in_air(drone, running_tasks) -> None:
    """
    Monitor if UAV is flying and cancel tasks after landing.
    
    Args:
        drone (dict): UAV system dictionary
        running_tasks (list): List of asyncio tasks to cancel when UAV lands
    """
    was_in_air = False

    try:
        async for is_in_air in drone["system"].telemetry.in_air():
            if is_in_air:
                was_in_air = True
                
            if was_in_air and not is_in_air:
                # UAV has landed after being in the air
                print(f"UAV-{drone['ID']} has landed, canceling tasks")
                
                # Cancel all running tasks
                for task in running_tasks:
                    if not task.done():
                        task.cancel()
                        try:
                            await task
                        except asyncio.CancelledError:
                            pass
                            
                # Clean up any remaining async generators
                await asyncio.get_event_loop().shutdown_asyncgens()
                return
                
    except Exception as e:
        print(f"Error in observe_is_in_air: {repr(e)}")


async def uav_fn_upload_mission(drone, mission_plan_file, verbose=False) -> None:
    """
    Upload a mission plan to a UAV.
    
    Args:
        drone (dict): UAV system dictionary
        mission_plan_file (str): Path to mission plan file with lat,lon coordinates
        verbose (bool): Whether to print upload progress
        
    Raises:
        FileNotFoundError: If mission plan file doesn't exist
    """
    if mission_plan_file is None:
        print("No mission plan file provided")
        return
        
    if not os.path.exists(mission_plan_file):
        raise FileNotFoundError(f"Mission plan file {mission_plan_file} not found")
    
    try:
        # Different handling for QGC plan files vs simple coordinate files
        if Path(mission_plan_file).suffix == ".plan":
            # TODO: Implement QGC plan file parsing
            print("QGC plan file format not yet supported")
            return
            
        # Read coordinates from file
        with open(mission_plan_file, "r") as f:
            mission_data = []
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    lat, lon = map(float, line.split(", "))
                    mission_data.append((lat, lon))
                except ValueError:
                    print(f"Invalid coordinate format: {line}")
                    
        if not mission_data:
            print("No valid coordinates found in mission file")
            return
            
        # Get mission altitude from UAV configuration
        height = drone["init_params"].get("altitude", 10.0)
        
        # Create mission items
        mission_items = []
        for lat, lon in mission_data:
            mission_items.append(
                MissionItem(
                    latitude_deg=lat,
                    longitude_deg=lon,
                    relative_altitude_m=height,
                    speed_m_s=1.0,
                    is_fly_through=False,
                    gimbal_pitch_deg=float("nan"),
                    gimbal_yaw_deg=float("nan"),
                    loiter_time_s=10,
                    acceptance_radius_m=float("nan"),
                    yaw_deg=float("nan"),
                    camera_action=MissionItem.CameraAction.NONE,
                    camera_photo_distance_m=float("nan"),
                    camera_photo_interval_s=float("nan"),
                    vehicle_action=MissionItem.VehicleAction.NONE,
                )
            )
            
        # Create and upload mission plan
        mission_plan = MissionPlan(mission_items)
        
        # print(f"UAV-{drone['ID']} uploading mission with {len(mission_items)} waypoints")
        
        if verbose:
            async for item in drone["system"].mission.upload_mission_with_progress(mission_plan):
                print(f"Upload progress: {item}")
        else:
            await drone["system"].mission.upload_mission(mission_plan)
            
        # print(f"UAV-{drone['ID']} mission upload complete")
        
    except Exception as e:
        print(f"Error uploading mission: {repr(e)}")


async def uav_fn_do_mission(drone, mission_plan_file) -> None:
    """
    Execute a complete UAV mission from takeoff to landing.
    
    Args:
        drone (dict): UAV system dictionary
        mission_plan_file (str): Path to mission file with coordinates
    """
    try:
        # Health check before mission
        # print(f"UAV-{drone['ID']} checking health before mission")
        await _check_uav_health(drone)
        
        # Clear any existing mission
        await drone["system"].mission.clear_mission()
        
        # Set up monitoring tasks
        print_mission_progress_task = asyncio.ensure_future(print_mission_progress(drone))
        running_tasks = [print_mission_progress_task]
        termination_task = asyncio.ensure_future(observe_is_in_air(drone, running_tasks))
        
        # Upload the mission
        await uav_fn_upload_mission(drone, mission_plan_file)
        await asyncio.sleep(1)
        
        # Connect to the UAV
        # print(f"UAV-{drone['ID']} connecting before mission")
        await drone["system"].connect(drone["system_address"])
        await asyncio.sleep(1)
        
        # Arm and take off
        # print(f"UAV-{drone['ID']} arming")
        await drone["system"].action.arm()
        await asyncio.sleep(2)
        
        # print(f"UAV-{drone['ID']} taking off")
        await drone["system"].action.takeoff()
        await asyncio.sleep(3)
        
        # Start the mission
        # print(f"UAV-{drone['ID']} starting mission")
        await drone["system"].mission.start_mission()
        
        # Wait for termination (landing)
        await termination_task
        
    except Exception as e:
        print(f"Error executing mission: {repr(e)}")
        
        # Try to cancel any running tasks
        try:
            for task in [print_mission_progress_task, termination_task]:
                if task and not task.done():
                    task.cancel()
        except:
            pass


async def _check_uav_health(drone):
    """
    Check if UAV is healthy enough for mission.
    
    Args:
        drone (dict): UAV system dictionary
        
    Raises:
        RuntimeError: If health check fails
    """
    max_checks = 10
    check_count = 0
    
    while check_count < max_checks:
        async for health in drone["system"].telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                # print(f"UAV-{drone['ID']} health check passed")
                return
                
            # Log specific issues
            issues = []
            if not health.is_global_position_ok:
                issues.append("no global position")
            if not health.is_home_position_ok:
                issues.append("no home position")
                
            print(f"UAV-{drone['ID']} health check issues: {', '.join(issues)}")
            check_count += 1
            await asyncio.sleep(1)
            break
            
    raise RuntimeError(f"UAV-{drone['ID']} failed health check after {max_checks} attempts")


# --------------------- RESCUE FUNCTIONS ---------------------

async def uav_rescue_process(drone, rescue_filepath):
    """
    Performs the UAV rescue operation.
    This asynchronous function carries out a rescue mission by navigating the drone to coordinates
    specified in the rescue file, performing a downward movement, and then returning to launch position.
    Args:
        drone (dict): A dictionary containing drone control interfaces and systems.
        rescue_fpath (str): File path to the rescue coordinates file. The file should contain
            latitude and longitude as comma-separated floats.
    Returns:
        None: This function doesn't return any value.
    Note:
        - The function reads rescue coordinates from a file (latitude, longitude).
        - Current implementation includes a 5-meter downward movement at the rescue location.
        - After completing the rescue operation, the drone returns to its launch location.
    """

    # await asyncio.sleep(1)
    print("---> [RESCUE PROCESS] Start going to rescue location at: ", end="")
    # await uav_fn_do_mission(drone, rescue_fpath)
    with open(rescue_filepath, "r") as rf:
        rescue_pos = rf.read().strip().split(", ")
    rescue_pos = list(map(float, rescue_pos))
    # print rescue position
    print(rescue_pos)
    
    # check if the drone is in the air, if not, connect to the drone
    # and arm it
    # and take off    
    # print("---> [RESCUE PROCESS] Arming drone.")
    # await drone["system"].action.arm()
    # await asyncio.sleep(1)
    
    # print("---> [RESCUE PROCESS] Taking off.")
    # await drone["system"].action.takeoff()
    # await asyncio.sleep(3)
    
    # async for position in drone["system"].telemetry.position():
    #     print("---> [RESCUE PROCESS] Current position: ", end="")
    #     print(f"({position.latitude_deg}, {position.longitude_deg})")
    #     drone["init_params"]["latitude"] = round(position.latitude_deg, 12)
    #     drone["init_params"]["longitude"] = round(position.longitude_deg, 12)
    #     break

    # go to the rescue position

    await uav_fn_goto_location(
        drone=drone,
        latitude=rescue_pos[0],
        longitude=rescue_pos[1],
    )
    # await uav_fn_do_mission(drone=drone, mission_plan_file=rescue_filepath)     

    print("---> [RESCUE PROCESS] Arrived at rescue location.")

    # Todo: do something here ==========================
    await asyncio.sleep(3)
    # NOTE: Change distance to go down here
    descending_distance = 5  # meters
    print("---> [RESCUE PROCESS] Start descending {} meters.".format(descending_distance))
    await uav_fn_goto_distance(drone, distance=descending_distance, direction="down")
    print("---> [RESCUE PROCESS] Reached rescue level, start dropping rescue kit.")
    await asyncio.sleep(1)
    # await uav_fn_control_gimbal(drone, control_value={"pitch": -90, "yaw": 0})
    print("---> [RESCUE PROCESS] Rescue kit dropped.")
    #
    print("---> [RESCUE PROCESS] Start ascending {} meters.".format(descending_distance))
    await uav_fn_goto_distance(drone, distance=descending_distance, direction="up")
    print("---> [RESCUE PROCESS] Reached initial level.")
    await asyncio.sleep(3)
    print("---> [RESCUE PROCESS] Mission completed!")
    print("---> [RESCUE PROCESS] Start returning to launch position.")
    # ===================================================

    await drone["system"].action.return_to_launch()

    return


async def uav_suspend_missions(drones, suspend_time=30):
    """
    Temporarily suspend multiple UAV missions for a specified duration.
    
    This function pauses missions for all specified drones, holds their positions,
    waits for the specified duration, and then resumes their missions.
    
    Args:
        drones (list): List of UAV system dictionaries
        suspend_time (int): Duration in seconds to suspend missions (default: 30)
        
    Returns:
        None
    """
    if not drones:
        print("---> [RESCUE PROCESS] No drones to suspend")
        return
        
    suspend_tasks = []
    for drone in drones:
        if not isinstance(drone, dict) or "ID" not in drone:
            print(f"---> [RESCUE PROCESS] Invalid drone object: {type(drone)}")
            continue
            
        suspend_tasks.append(_suspend_single_mission(drone, suspend_time))
        
    if suspend_tasks:
        await asyncio.gather(*suspend_tasks)
    else:
        print("---> [RESCUE PROCESS] No valid drones to suspend")

async def _suspend_single_mission(drone, suspend_time):
    """Suspend a single UAV's mission and resume after specified time."""
    drone_id = drone.get("ID", "unknown")
    
    try:
        # Disable detection during suspension
        drone["detection_enable"] = False
        print(f"---> [RESCUE PROCESS] UAV-{drone_id} suspending mission for {suspend_time} seconds")
        
        # Pause mission execution
        await drone["system"].mission.pause_mission()
        
        # Hold position
        await drone["system"].action.hold()
        
        # Wait for the specified duration
        await asyncio.sleep(suspend_time)
        
        # Resume mission
        print(f"---> [RESCUE PROCESS] UAV-{drone_id} resuming mission")
        await drone["system"].mission.start_mission()
        
        # Re-enable detection
        drone["detection_enable"] = True
        
    except Exception as e:
        print(f"---> [RESCUE PROCESS] Error suspending UAV-{drone_id}: {repr(e)}")
        # Try to re-enable detection even if there was an error
        drone["detection_enable"] = True


def select_mission_plan(mission_plan_files):
    """
    Select an appropriate mission plan from available files.
    
    Args:
        mission_plan_files (list): List of mission plan file paths
        
    Returns:
        str: Selected mission plan file path, or None if list is empty
        
    Note:
        The current implementation selects the first file in the list,
        but this function can be extended with more sophisticated selection logic.
    """
    if not mission_plan_files:
        print("---> [RESCUE PROCESS] No mission plan files available")
        return None
        
    # Log the available mission plans
    if len(mission_plan_files) > 1:
        print(f"---> [RESCUE PROCESS] Multiple mission plans available ({len(mission_plan_files)})")
        
    # Current implementation: select the first file
    # This could be extended with more sophisticated selection logic:
    # - Select based on priority/timestamp
    # - Choose closest target
    # - Select based on target type or confidence score
    
    selected_plan = mission_plan_files.pop(0)
    print(f"---> [RESCUE PROCESS] Selected mission plan: {os.path.basename(selected_plan)}")
    
    # Return a copy of the first file path
    return selected_plan


def clear_mission_logs(uav_index, save_dir):
    """
    Clear mission logs for a specific UAV.
    
    This removes rescue position and detection log files for cleanup
    after mission completion or when resetting.
    
    Args:
        uav_index (int): The UAV index
        save_dir (str): Directory containing log files
        
    Returns:
        None
    """
    # Ensure valid parameters
    if not isinstance(uav_index, int) or not save_dir:
        print(f"Invalid parameters: uav_index={uav_index}, save_dir={save_dir}")
        return
        
    try:
        # Define log file paths
        rescue_file = f"{save_dir}/logs/rescue_pos/rescue_pos_uav_{uav_index}.log"
        detection_file = f"{save_dir}/logs/detected_pos/detection_pos_uav_{uav_index}.log"
        
        # Remove rescue position file if it exists
        if os.path.exists(rescue_file):
            os.remove(rescue_file)
            print(f"Removed rescue log: {rescue_file}")
            
        # Remove detection log file if it exists
        if os.path.exists(detection_file):
            os.remove(detection_file)
            print(f"Removed detection log: {detection_file}")
            
    except Exception as e:
        print(f"Error clearing mission logs for UAV-{uav_index}: {repr(e)}")


def export_points_to_gps_log(uav_index, detected_pos, frame_shape, uav_gps):
    """
    Convert pixel coordinates to GPS coordinates and log detection information.
    
    This function translates a detection in image coordinates to real-world GPS
    coordinates based on the UAV's position, altitude, and camera parameters.
    It writes the coordinates to rescue position and detection log files.
    
    Args:
        uav_index (int): The UAV index
        detected_pos (tuple): Pixel coordinates (x, y) of detected target
        frame_shape (tuple): Video frame dimensions (height, width, channels)
        uav_gps (list): UAV GPS coordinates [latitude, longitude, altitude]
        
    Returns:
        list: Information about the conversion (currently unused)
    """
    # Validate inputs
    if not all(isinstance(x, (int, float)) for x in detected_pos) or len(detected_pos) != 2:
        print(f"Invalid detected position: {detected_pos}")
        return
        
    if not all(isinstance(x, float) for x in uav_gps) or len(uav_gps) != 3:
        print(f"Invalid GPS coordinates: {uav_gps}")
        return
        
    try:
        # Extract coordinates and dimensions
        target_pixel_x, target_pixel_y = detected_pos
        image_height, image_width, _ = frame_shape
        uav_lat, uav_lon, uav_alt = uav_gps

        # Camera and field-of-view parameters
        fov_horizontal = 80.0  # Camera horizontal FOV in degrees
        aspect_ratio = image_height / image_width
        
        # Calculate vertical FOV from horizontal FOV and aspect ratio
        fov_vertical = 2 * math.degrees(
            math.atan(math.tan(math.radians(fov_horizontal) / 2) * aspect_ratio)
        )

        # Calculate physical size of the area covered by the camera
        fov_rad_horizontal = math.radians(fov_horizontal)
        ground_width = 2 * uav_alt * math.tan(fov_rad_horizontal / 2)
        pixel_size = ground_width / image_width  # Size of pixel in meters

        # Calculate distance and angle from center of frame
        center_pixel = (image_width / 2, image_height / 2)
        dx = (target_pixel_x - center_pixel[0]) * pixel_size
        dy = (target_pixel_y - center_pixel[1]) * pixel_size
        distance = math.sqrt(dx**2 + dy**2)
        angle = math.atan2(dy, dx)
        angle_deg = math.degrees(angle)

        # Calculate target GPS coordinates using geodesic calculations
        geod = Geodesic.WGS84
        gps_result = geod.Direct(uav_lat, uav_lon, angle_deg, distance)
        target_lat = gps_result["lat2"]
        target_lon = gps_result["lon2"]

        # Create log directories if they don't exist
        rescue_dir = f"{SRC_DIR}/logs/rescue_pos"
        detection_dir = f"{SRC_DIR}/logs/detected_pos"
        os.makedirs(rescue_dir, exist_ok=True)
        os.makedirs(detection_dir, exist_ok=True)

        # Write rescue position file (currently using UAV position rather than calculated position)
        rescue_filepath = f"{rescue_dir}/rescue_pos_uav_{uav_index}.log"
        with open(rescue_filepath, "w") as f:
            # Note: Currently using UAV position rather than calculated target position
            # This can be changed to f"{target_lat}, {target_lon}\n" to use calculated position
            # f.write(f"{target_lat}, {target_lon}\n")
            f.write(f"{uav_lat}, {uav_lon}\n")
            
        # Log detection with timestamp
        time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        detection_filepath = f"{detection_dir}/detection_pos_uav_{uav_index}.log"
        with open(detection_filepath, "a") as f:
            f.write(
                f"{time_stamp}, {target_pixel_x}, {target_pixel_y}, "
                f"{uav_lat}, {uav_lon}, {uav_alt}\n"
            )
            
        print(f"Exported detection from UAV-{uav_index} to GPS log files")
        
    except Exception as e:
        print(f"Error exporting detection to GPS log: {repr(e)}")


# ! Not used
async def uav_fn_swarm_goto(drones, txt_file_path):
    """NOTE: Not used
    Asynchronously directs a UAV to a specified location based on coordinates read from a file.

    Args:
        uav_index (int): The index of the UAV in the UAVs list.
        *args: Additional arguments (not used in this function).

    Returns:
        None
    """

    with open(txt_file_path, "r") as file:
        content = file.read()
        lat_detect, lon_detect = map(float, content.strip().split(", "))

    if len(drones) == 1:
        uav_fn_goto_location(drones[0], lat_detect, lon_detect)
    else:
        await asyncio.gather(
            *[uav_fn_goto_location(drone, lat_detect, lon_detect) for drone in drones]
        )


# ! Not used
async def swarm_algorithm(drones, n_swarms, txt_file_path):
    """NOTE: This function is not used now, modify later if needed.
    Compares the distance of multiple UAVs to a detected location and directs the closest ones to move.

    Args:
        num_UAVs (int): The number of UAVs to compare and control.
        *args: Additional arguments (not used).

    Returns:
        None

    Reads the detected location from a file, retrieves UAV positions, calculates distances, sorts UAVs by distance, and directs the closest ones to move.
    """

    with open(txt_file_path, "r") as file:
        content = file.read()
        lat_detect, lon_detect = map(float, content.strip().split(", "))

    distances = []
    latitudes = []
    longitudes = []

    for drone in drones:
        async for position in drone["system"].telemetry.position():
            latitudes.append(position.latitude_deg)
            longitudes.append(position.longitude_deg)
            break

        distances.append(calculate_distance(latitudes[-1], longitudes[-1], lat_detect, lon_detect))

    # sort drones by distance
    sorted_drones = [drone for _, drone in sorted(zip(distances, drones))]
    # selected
    await uav_fn_swarm_goto(sorted_drones[:n_swarms], txt_file_path)


# ? In development..., currently not used
def convert_pointsFile_to_missionPlan(pointsFile, default_height=10):
    """
    Converts a points file to a mission plan file.
    
    This function reads GPS coordinates from a points file and creates a mission
    plan file in the appropriate format for UAV missions.
    
    Args:
        pointsFile (str): Path to the file containing GPS points.
        default_height (int, optional): The default altitude in meters for waypoints.
                                      Defaults to 10.
    
    Returns:
        None
    
    Note:
        - The points file should contain latitude and longitude as comma-separated values
        - The mission plan is saved to ./mission/mission_plan.json
        - Uses templates from ./mission/ directory to create the mission plan
    """
    
    # convert ./src/logs/points/points1.txt to ./src/data/mission plan
    # item template from data/mission/single_item_obj.json

    item_template = json.load(open("./mission/single_item_obj.json", "r"))
    mission_template = json.load(open("./mission/mission_template.json", "r"))
    plan_template = json.load(open("./mission/plan_template.json", "r"))

    with open(pointsFile, "r") as f:
        for line in f:
            lat, lon = map(float, line.strip().split(", "))
            # https://mavlink.io/en/messages/common.html#mav_commands

            item_template["params"][4] = lat
            item_template["params"][5] = lon
            item_template["params"][6] = default_height
            mission_template["items"].append(item_template)

    plan_template["mission"] = mission_template

    with open("./mission/mission_plan.json", "w") as f:
        json.dump(plan_template, f, indent=4)
    pass
    pass
