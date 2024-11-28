import asyncio
import json
import math

import cv2
from mavsdk.gimbal import ControlMode, GimbalMode
from mavsdk.offboard import (
    ActuatorControl,
    ActuatorControlGroup,
    Offboard,
    OffboardError,
)
from tqdm import tqdm

# cSpell:ignore asyncio, asyncgen tqdm offboard mavsdk


def calculate_distance(lat1, lon1, lat2, lon2) -> float:
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


async def uav_fn_get_params(drone, list_params=None, save_path=None) -> dict:
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

        # write to file with .params format
        if save_path is not None:
            with open(save_path, "w") as wf:
                for i in tqdm(range(len(int_param_names))):
                    wf.write(f"{int_param_names[i]}\t{int_param_values[i]}\n")
                for i in tqdm(range(len(float_param_names))):
                    wf.write(f"{float_param_names[i]}\t{float_param_values[i]}\n")
                for i in tqdm(range(len(custom_param_names))):
                    wf.write(f"{custom_param_names[i]}\t{custom_param_values[i]}\n")

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
        parameters = {}
        with open(param_file, "r") as param_file:
            print("Uploading Parameters... Please do not arm the vehicle!")
            for line in tqdm(param_file, unit="lines"):
                if line.startswith("#"):
                    continue

                columns = line.strip().split("\t")
                # vehicle_id = columns[0]
                # component_id = columns[1]
                name = columns[2]
                value = columns[3]
                # type = columns[4]
                parameters[name] = value

    # set parameters from parameters
    for param_name, param_value in parameters.items():
        if param_name in int_param_names:
            await param_plugin.set_param_int(param_name, int(param_value))
        elif param_name in float_param_names:
            await param_plugin.set_param_float(param_name, float(param_value))
        elif param_name in custom_param_names:
            await param_plugin.set_param_custom(param_name, param_value)


async def uav_fn_goto_location(drone, latitude, longitude, altitude=None, error=1e-10) -> None:
    # Go to location
    if altitude is None:
        async for position in drone["system"].telemetry.position():
            altitude = position.relative_altitude_m
            break
    async for position in drone["system"].telemetry.position():
        current_latitude = position.latitude_deg
        current_longitude = position.longitude_deg
        if abs(current_latitude - latitude) < error and abs(current_longitude - longitude) < error:
            print("Already at the location")
            break
        await drone["system"].action.goto_location(latitude, longitude, altitude, 0)
        break
    return


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


# * develop later
def convert_points_to_gps(detected_pos, frame_shape, uav_gps) -> list:
    x, y = detected_pos
    h, w, c = frame_shape
    lat, lon, alt = uav_gps
    # * ===== Modify here =============================

    # * ================================================
    return lat, lon


# -----------------------------------------------------


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
