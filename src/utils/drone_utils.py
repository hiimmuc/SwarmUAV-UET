import asyncio
import json


async def print_mission_progress(drone):
    async for mission_progress in drone["system"].mission.mission_progress():
        print(
            f"Mission UAV-{drone['ID']} progress: "
            f"{mission_progress.current}/"
            f"{mission_progress.total}"
        )


async def observe_is_in_air(drone, running_tasks):
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


def convert_pointsFile_to_missionPlan(pointsFile):
    # convert ./src/logs/points/points1.txt to ./src/data/mission plan

    with open(pointsFile, "r") as f:
        points = f.readlines()

    pass
