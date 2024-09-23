
from typing import Dict, Any, Optional, Union
from mavsdk import System

from mavsdk.mission import (MissionItem, MissionPlan)
from asyncqt import QEventLoop, asyncSlot
import asyncio


class Drone(System):
    def __init__(self, id, system_address=None,  port=8888, **kwargs) -> None:
        System.__init__(self, mavsdk_server_address="localhost", port=port)
        self.id = id
        self.system_address = system_address
        self.openClose_status = False
        self.battery_level = 0.0
        self.arming_status = False

    # basic functions

    async def getParameters(self) -> Dict[str, Any]:
        parameters = {}
        parameters["MIS_TAKEOFF_ALT"] = await self.param.get_param_float("MIS_TAKEOFF_ALT")
        parameters["MPC_TKO_SPEED"] = await self.param.get_param_float("MPC_TKO_SPEED")
        parameters["MPC_LAND_SPEED"] = await self.param.get_param_float("MPC_LAND_SPEED")
        parameters["COM_DISARM_LAND"] = await self.param.get_param_float("COM_DISARM_LAND")
        parameters["MC_YAW_P"] = await self.param.get_param_float("MC_YAW_P")

        return parameters

    async def updateParameters(self, parameters: Dict[str, Any]) -> None:
        await self.param.set_param_float("MPC_TKO_SPEED", parameters["MPC_TKO_SPEED"])
        await self.param.set_param_float("MPC_LAND_SPEED", parameters["MPC_LAND_SPEED"])
        await self.param.set_param_float("COM_DISARM_LAND", parameters["COM_DISARM_LAND"])
        await self.param.set_param_float("MC_YAW_P", parameters["MC_YAW_P"])
        new_parameters = await self.getParameters()
        return new_parameters

    async def get_altitude(self, *args) -> Optional[float]:
        gps_position = {}
        async for position in self.telemetry.position():
            relative_altitude = round(position.relative_altitude_m, 1)
            absolute_altitude = round(position.absolute_altitude_m, 1)
            latitude, longitude = position.latitude_deg, position.longitude_deg
            gps_position.setdefault(
                'relative_altitude', []).append(relative_altitude)
            gps_position.setdefault(
                'absolute_altitude', []).append(absolute_altitude)
            gps_position.setdefault('latitude', []).append(latitude)
            gps_position.setdefault('longitude', []).append(longitude)
        return gps_position

    async def getFlightMode(self, *args) -> Optional[str]:
        modes = []
        async for mode in self.telemetry.flight_mode():
            if str(mode) == "RETURN_TO_LAUNCH":
                mod = "RTL"
            else:
                mod = str(mode)
            modes.append(mod)
        return modes

    async def getBatteryLevel(self, *args) -> Optional[float]:
        battery_infos = {}
        async for battery in self.telemetry.battery():
            v = round(battery.voltage_v, 1)
            remaining_percent = round(battery.remaining_percent, 1)

            battery_infos.setdefault('voltage', []).append(v)
            battery_infos.setdefault(
                'remaining_percent', []).append(remaining_percent)

        return self.battery_level

    async def getArmStatus(self, *args) -> Optional[bool]:
        arm_status = []
        async for arming_status in self.telemetry.armed():
            arm = "ARMED" if arming_status else "Disarmed"
            arm_status.append(arm)
        return arm_status

    async def getGPS(self, *args) -> None:
        gps_infos = {}
        async for gps in self.telemetry.gps_info():
            satellite = gps.num_satellites
            gps_fix = gps.fix_type
            gps_infos.setdefault('satellite', []).append(satellite)
            gps_infos.setdefault('fix_type', []).append(gps_fix)
        return gps_infos

    # control functions

    async def Connect(self, *args) -> None:
        await self.connect(self.system_address)
        await self.action.set_maximum_speed(1.0)

    async def arming(self, *args) -> None:
        await self.action.arm()
        self.arming_status = True
        # Note: arm 5s, and then automatically disarm

    async def disarm(self, *args) -> None:
        await self.action.disarm()
        self.arming_status = False

    async def takeOff(self, altitude=5, *args) -> None:
        if not self.arming_status:
            await self.arming()
        await self.action.set_takeoff_altitude(altitude=altitude)
        await self.action.takeoff()

    async def land(self, *args) -> None:
        await self.action.land()

    # complex
    async def performMission(self, *args) -> None:
        if not self.arming_status:
            await self.arming()
        await self.mission.start_mission()
        async for mission_progress in self.mission.mission_progress():
            if mission_progress.current == mission_progress.total:
                await self.returnToLaunchAltitude()
                break

    async def pauseMission(self, *args) -> None:
        await self.mission.pause_mission()
        pass

    async def uploadMission(self, missionReadFile=None, height=5, *args) -> None:
        missionPointsFile = f'./logs/points/points_uav_{self.id}.txt'
        with open(missionReadFile, 'r') as f:
            file_content = f.read()
            print("File content:", file_content)

        mission_items = []

        with open(missionPointsFile, 'r') as f:
            for line in f:
                lat1, lon1 = map(
                    float, line.strip().split(', '))
                mission_item = MissionItem(lat1,
                                           lon1,
                                           height,
                                           float('nan'),
                                           False,
                                           float('nan'),
                                           float('nan'),
                                           MissionItem.CameraAction.NONE,
                                           10,
                                           float('nan'),
                                           float('nan'),
                                           float('nan'),
                                           float('nan'),
                                           MissionItem.VehicleAction.NONE)
                mission_items.append(mission_item)
        mission_plan = MissionPlan(mission_items)
        await asyncio.sleep(1)
        await self.mission.set_return_to_launch_after_mission(True)
        await self.mission.upload_mission(mission_plan)

    async def goToPoint(self, latitude, longitude, * args) -> None:
        async for position in self.telemetry.position():
            height = position.absolute_altitude_m
            await self.action.goto_location(latitude, longitude, height, 0)

    async def returnToLaunchAltitude(self, altitude, *args) -> None:
        await self.action.set_return_to_launch_altitude(altitude)
        await self.action.return_to_launch()

    # camera

    async def turnOnCamera(self, *args) -> None:
        pass

    async def turnOffCamera(self, *args) -> None:
        pass

    async def getImageStream(self, *args) -> None:
        pass

    async def getDistance(self, *args) -> None:
        pass


if __name__ == '__main__':
    drone = Drone(id='1', system_address='udp://:14541', port=50060)
    drone.Connect()
    drone.arming()
    drone.takeOff()
