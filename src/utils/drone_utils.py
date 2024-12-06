import asyncio
import json
import math
from pathlib import Path

import cv2
from mavsdk.gimbal import ControlMode, GimbalMode
from mavsdk.mission import MissionItem, MissionPlan
from mavsdk.offboard import (
    ActuatorControl,
    ActuatorControlGroup,
    Offboard,
    OffboardError,
)

# cSpell:ignore asyncio, asyncgen  offboard mavsdk
SRC_DIR = Path(__file__).resolve().parent.parent


def calculate_distance(lat1, lon1, lat2, lon2) -> float:
    """
    Calculate the great-circle distance between two points on the Earth's surface.
    This function uses the Haversine formula to calculate the distance between two points
    specified by their latitude and longitude in decimal degrees.
    Args:
        lat1 (float): Latitude of the first point in decimal degrees.
        lon1 (float): Longitude of the first point in decimal degrees.
        lat2 (float): Latitude of the second point in decimal degrees.
        lon2 (float): Longitude of the second point in decimal degrees.
    Returns:
        float: The distance between the two points in meters.
    """

    R = 6378000  # radius of Earth in meters
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)
    ) * math.sin(d_lon / 2) * math.sin(d_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


async def print_mission_progress(drone) -> None:
    async for mission_progress in drone["system"].mission.mission_progress():
        print(
            f"Mission UAV-{drone['ID']} progress: "
            f"{mission_progress.current}/"
            f"{mission_progress.total}"
        )


async def observe_is_in_air(drone, running_tasks) -> None:
    """Monitors whether the drone is flying or not and
    returns after landing"""

    was_in_air = False

    async for is_in_air in drone["system"].telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()

            return


async def uav_fn_export_params(drone, save_path) -> None:
    """
    Asynchronously exports UAV parameters to a specified file.
    This function retrieves all parameters from the UAV's parameter plugin and writes them to a file at the specified save path. The parameters are categorized into integer, float, and custom parameters, and each category is written to the file with the parameter name and value.
    Args:
        drone (dict): A dictionary containing the UAV system and its plugins.
        save_path (str): The file path where the parameters will be saved. If None, the function will return immediately.
    Returns:
        None
    """

    if save_path is None:
        return

    param_plugin = drone["system"].param

    params = await param_plugin.get_all_params()

    int_params = params.int_params
    float_params = params.float_params
    custom_params = params.custom_params

    int_param_names = [p.name for p in int_params]
    float_param_names = [p.name for p in float_params]
    custom_param_names = [p.name for p in custom_params]

    int_param_values = [p.value for p in int_params]
    float_param_values = [p.value for p in float_params]
    custom_param_values = [p.value for p in custom_params]

    with open(save_path, "w") as wf:
        for i in range(len(int_param_names)):
            wf.write(f"{int_param_names[i]}\t{int_param_values[i]}\n")
        for i in range(len(float_param_names)):
            wf.write(f"{float_param_names[i]}\t{float_param_values[i]}\n")
        for i in range(len(custom_param_names)):
            wf.write(f"{custom_param_names[i]}\t{custom_param_values[i]}\n")

    return


def uav_fn_import_params(load_path) -> dict:
    """
    Imports UAV parameters from a file.
    Args:
        load_path (str): The path to the file containing the UAV parameters.
    Returns:
        dict: A dictionary containing the UAV parameters with parameter names as keys and their corresponding values.
            Returns an empty dictionary if the file is empty or None if the load_path is None.
    Notes:
        - The file should be a tab-separated values file.
        - Lines starting with '#' are considered comments and are ignored.
        - Each line in the file should contain the following columns: vehicle_id, component_id, name, value, type.
    """

    if load_path is None:
        return
    parameters = {}

    with open(load_path, "r") as rf:
        for line in rf.readlines():
            if line.startswith("#"):
                continue

            columns = line.strip().split("\t")
            # columns: vehicle_id, component_id, name, value, type
            name = columns[2]
            value = columns[3]

            parameters[name] = value

    return parameters


async def uav_fn_get_params(drone, list_params=None) -> dict:
    """
    Asynchronously retrieves UAV parameters.
    This function fetches parameters from a UAV system, either all parameters or a specified list of parameters.
    Args:
        drone (dict): A dictionary containing the UAV system, with the key "system" pointing to the system object.
        list_params (list, optional): A list of parameter names to retrieve. If None, all parameters are retrieved.
    Returns:
        dict: A dictionary where the keys are parameter names and the values are the corresponding parameter values.
    Raises:
        Exception: If there is an issue retrieving the parameters from the UAV system.
    """

    parameters = {}

    param_plugin = drone["system"].param

    params = await param_plugin.get_all_params()

    int_params = params.int_params
    float_params = params.float_params
    custom_params = params.custom_params

    int_param_names = [p.name for p in int_params]
    float_param_names = [p.name for p in float_params]
    custom_param_names = [p.name for p in custom_params]

    if list_params is None:  # if list_params is not provided, get all parameters
        # get all parameters
        int_param_values = [p.value for p in int_params]
        float_param_values = [p.value for p in float_params]
        custom_param_values = [p.value for p in custom_params]

        param_names = int_param_names + float_param_names + custom_param_names
        param_values = int_param_values + float_param_values + custom_param_values
    else:
        param_names = list_params
        param_values = []
        for param_name in param_names:
            if param_name in int_param_names:
                param = await param_plugin.get_param_int(param_name)
            elif param_name in float_param_names:
                param = await param_plugin.get_param_float(param_name)
            elif param_name in custom_param_names:
                param = await param_plugin.get_param_custom(param_name)
            param_values.append(param)

    for i in range(len(param_names)):
        parameters[param_names[i]] = param_values[i]

    return parameters


async def uav_fn_set_params(drone, parameters=None, param_file=None) -> None:
    """
    Asynchronously sets parameters for a UAV using the provided drone system.
    Parameters:
    - drone (dict): A dictionary containing the drone system, which includes the parameter plugin.
    - parameters (dict, optional): A dictionary of parameters to set. If not provided, parameters will be read from the param_file.
    - param_file (str, optional): Path to a file containing parameters. Used if parameters are not provided.
    Returns:
    - None
    This function retrieves all current parameters from the drone system and sets new parameters based on the provided
    parameters dictionary or the parameter file. It supports setting integer, float, and custom parameters.
    """

    param_plugin = drone["system"].param

    params = await param_plugin.get_all_params()

    float_params = params.float_params
    int_params = params.int_params
    custom_params = params.custom_params

    int_param_names = [p.name for p in int_params]
    float_param_names = [p.name for p in float_params]
    custom_param_names = [p.name for p in custom_params]

    if (parameters is None) and (
        param_file is not None
    ):  # if parameters is not provided, read from param_file
        parameters = uav_fn_import_params(param_file)

    # set parameters from parameters
    for param_name, param_value in parameters.items():
        if param_name in int_param_names:
            await param_plugin.set_param_int(param_name, int(param_value))
        elif param_name in float_param_names:
            await param_plugin.set_param_float(param_name, float(param_value))
        elif param_name in custom_param_names:
            await param_plugin.set_param_custom(param_name, param_value)


async def uav_fn_goto_location(drone, latitude, longitude, altitude=None) -> None:
    """
    Asynchronously commands the UAV to go to a specified location.
    Parameters:
        drone (dict): A dictionary containing the UAV system.
        latitude (float): The latitude of the target location.
        longitude (float): The longitude of the target location.
        altitude (float, optional): The absolute altitude of the target location. If not provided, the UAV's home altitude is used.
    Returns:
        None
    """

    # Go to location
    if altitude is None:
        async for position in drone["system"].telemetry.home():
            altitude = position.absolute_altitude_m
            break
    await drone["system"].action.goto_location(latitude, longitude, altitude, 0)

    return


async def uav_fn_upload_mission(drone, mission_plan_file) -> None:
    """
    Uploads a mission plan to the UAV.
    Args:
        drone (dict): A dictionary containing drone parameters, including initial parameters such as altitude.
        mission_plan_file (str): The path to the mission plan file. The file can be a .plan file or a text file
                                containing latitude and longitude coordinates separated by commas.
    Returns:
        MissionPlan: An instance of the MissionPlan class containing the mission items to be uploaded to the UAV.
                    Returns None if the mission_plan_file is None.
    Raises:
        FileNotFoundError: If the mission_plan_file does not exist.
        ValueError: If the mission_plan_file contains invalid data.
    """

    if mission_plan_file is None:
        return
    elif Path(mission_plan_file).suffix == ".plan":
        pass
    else:
        with open(mission_plan_file, "r") as f:
            mission_data = [list(map(float, line.strip().split(", "))) for line in f.readlines()]

    height = drone["init_params"]["altitude"]
    mission_items = []
    for lat, lon in mission_data:
        mission_items.append(
            MissionItem(
                latitude_deg=lat,
                longitude_deg=lon,
                relative_altitude_m=height,
                speed_m_s=1.0,  # Speed to use after this mission item (in metres/second)
                is_fly_through=False,  # True for fly through, False for reach
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
    mission_plan = MissionPlan(mission_items)
    await drone["system"].mission.upload_mission(mission_plan)
    return


async def uav_fn_do_mission(drone, mission_plan_file) -> None:
    """
    Executes a mission plan for a UAV (Unmanned Aerial Vehicle).
    This function uploads a mission plan to the UAV, arms the UAV, takes off,
    and starts the mission. It also creates tasks to monitor mission progress
    and observe if the UAV is in the air.
    Args:
        drone (dict): A dictionary containing the UAV system components.
        mission_plan_file (str): The file path to the mission plan.
    Returns:
        None
    """

    # create tasks for monitoring mission progress and observing if the UAV is in the air
    print_mission_progress_task = asyncio.ensure_future(print_mission_progress(drone))
    running_tasks = [print_mission_progress_task]
    termination_task = asyncio.ensure_future(observe_is_in_air(drone, running_tasks))
    #
    await uav_fn_upload_mission(drone, mission_plan_file)
    await asyncio.sleep(1)
    #
    await drone["system"].connect(drone["system_address"])
    await asyncio.sleep(1)
    await drone["system"].action.arm()
    await asyncio.sleep(2)
    await drone["system"].action.takeoff()
    await asyncio.sleep(3)
    # await drone["system"].action.set_current_speed(2.0)
    #
    await drone["system"].mission.start_mission()
    #
    await termination_task
    return


async def uav_fn_overwrite_params(drone, parameters) -> None:
    """
    Overwrites the UAV parameters with the provided values.
    Args:
        drone (dict): A dictionary containing the drone system.
        parameters (dict): A dictionary containing the parameters to be set.
            Expected keys:
                - "RTL_AFTER_MS": Return to launch after mission (int or float).
                - "GND_SPEED_MAX": Maximum ground speed (int or float).
                - "MIS_TAKEOFF_ALT": Takeoff altitude (int or float).
                - "CURRENT_SPEED": Current speed (int or float).
    Returns:
        None
    """

    # set return to launch after mission
    await drone["system"].mission.set_return_to_launch_after_mission(parameters["RTL_AFTER_MS"])
    # maximum speed
    await drone["system"].action.set_maximum_speed(parameters["GND_SPEED_MAX"])
    #
    await drone["system"].action.set_takeoff_altitude(parameters["MIS_TAKEOFF_ALT"])
    #
    await drone["system"].action.set_return_to_launch_altitude(parameters["MIS_TAKEOFF_ALT"])
    #
    await drone["system"].action.set_current_speed(parameters["CURRENT_SPEED"])
    #
    # <...>


async def uav_fn_goto_distance(drone, distance, direction):
    """
    Asynchronously moves the UAV to a specified distance in a given direction.

    Args:
        uav_index (int): The index of the UAV in the UAVs list.
        direction (str): The direction to move the UAV. Can be 'forward', 'backward', 'left', 'right', 'up', or 'down'.
        distance (float): The distance to move the UAV in meters.

    Returns:
        None

    Raises:
        KeyError: If the UAV index is not found in the UAVs list.
        ValueError: If the direction is not one of the specified directions.

    Notes:
        - The function calculates the new position based on the current position and the specified distance.
        - The Earth's radius (r_earth) is assumed to be 6378137 meters.
        - The function only moves the UAV if its connection status is active.
        - The function uses the UAV's telemetry data to get the current position and then calculates the new position.
        - The function sends the UAV to the new calculated position using the `goto_location` method.
    """
    r_earth = 6378137

    lat, lon, alt = 0, 0, 0
    initial_lat, initial_lon, initial_alt = 0, 0, 0
    async for position in drone["system"].telemetry.position():
        if initial_lat == 0 and initial_lon == 0 and initial_alt == 0:
            initial_lat = position.latitude_deg
            initial_lon = position.longitude_deg
            initial_alt = position.absolute_altitude_m

        lat = position.latitude_deg
        lon = position.longitude_deg
        alt = position.absolute_altitude_m

        if direction == "forward":
            lat = initial_lat + (distance / r_earth) * (180 / math.pi)
        elif direction == "backward":
            lat = initial_lat - (distance / r_earth) * (180 / math.pi)
        elif direction == "left":
            lon = initial_lon - (distance / (r_earth * math.cos(math.pi * initial_lat / 180))) * (
                180 / math.pi
            )
        elif direction == "right":
            lon = initial_lon + (distance / (r_earth * math.cos(math.pi * initial_lat / 180))) * (
                180 / math.pi
            )
        elif direction == "up":
            alt = initial_alt + distance
        elif direction == "down":
            alt = initial_alt - distance
        else:
            print("Invalid direction")
            break
        # go to the new position
        await drone["system"].action.goto_location(lat, lon, alt, 0)
        break
    return


async def uav_fn_offboard_set_actuator(drone, group, controls):
    """Set actuator control with offboard mode."""
    nan = float("nan")
    offsets1 = [nan] * 8  # 8 actuator control channels
    offsets2 = [nan] * 8  # 8 actuator control channels

    await drone["system"].action.arm()

    await drone["system"].offboard.set_actuator_control(
        ActuatorControl([ActuatorControlGroup(offsets1), ActuatorControlGroup(offsets2)])
    )

    print("-- Starting offboard")
    try:
        await drone["system"].offboard.start()
    except OffboardError as error:
        print(
            f"Starting offboard mode failed with error code: \
            {error._result.result}"
        )
        print("-- Disarming")
        await drone["system"].action.disarm()
        return

    if group == 0:
        await drone["system"].offboard.set_actuator_control(
            ActuatorControl([ActuatorControlGroup(controls), ActuatorControlGroup(offsets2)])
        )
    elif group == 1:
        await drone["system"].offboard.set_actuator_control(
            ActuatorControl([ActuatorControlGroup(offsets1), ActuatorControlGroup(controls)])
        )

    await asyncio.sleep(2)

    print("-- Stopping offboard")
    try:
        await drone["system"].offboard.stop()
    except OffboardError as error:
        print(
            f"Stopping offboard mode failed with error code: \
            {error._result.result}"
        )
    pass


async def uav_fn_control_gimbal(drone, control_value={"pitch": 0, "yaw": 0}):
    """Control the gimbal of the UAV."""
    await drone["system"].gimbal.take_control(
        control_mode=ControlMode.PRIMARY
    )  # ControlMode.PRIMARY or ControlMode.SECONDARY
    await drone["system"].gimbal.set_mode(
        GimbalMode.YAW_FOLLOW
    )  # GimbalMode.YAW_FOLLOW or GimbalMode.YAW_LOCK
    await drone["system"].gimbal.set_pitch_and_yaw(control_value["pitch"], control_value["yaw"])
    await asyncio.sleep(2)
    await drone["system"].gimbal.release_control()


# -----------------------------------------------------


# ? In development...
def convert_points_to_gps(uav_index, detected_pos, frame_shape, uav_gps) -> list:
    x, y = detected_pos
    h, w, c = frame_shape
    lat, lon, alt = uav_gps
    # * ===== Modify here =============================
    rescue_filepath = f"{SRC_DIR}/logs/rescue_pos/rescue_pos_uav_{uav_index}.log"
    with open(rescue_filepath, "w") as f:
        f.write(f"{lat}, {lon}\n")
    # * ================================================
    return lat, lon


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


# ? In development...
def convert_pointsFile_to_missionPlan(pointsFile, default_height=10):
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
