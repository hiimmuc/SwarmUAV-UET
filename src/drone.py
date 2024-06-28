
from typing import Dict, Any, Optional, Union


class Drone:
    def __init__(self, *args,) -> None:
        pass

    # basic
    async def getParameters(self) -> Dict[str, Any]:
        pass

    async def updateParameters(self, parameters: Dict[str, Any]) -> None:
        pass

    async def connect(self, *args) -> None:
        pass

    async def arming(self, *args) -> None:
        pass

    async def disarm(self, *args) -> None:
        pass

    async def takeOff(self, *args) -> None:
        pass

    async def land(self, *args) -> None:
        pass

    async def getGPS(self, *args) -> None:
        pass

    # complex
    async def performMission(self, *args) -> None:
        pass

    async def pauseMission(self, *args) -> None:
        pass

    async def uploadMission(self, *args) -> None:
        pass

    async def goToPoint(self, latitude, longitude, * args) -> None:
        pass

    async def returnToLaunchAltitude(self, altitude, *args) -> None:
        pass

    # camera
    async def turnOnCamera(self, *args) -> None:
        pass

    async def getImageStream(self, *args) -> None:
        pass

    async def getDistance(self, *args) -> None:
        pass

    async def turnOffCamera(self, *args) -> None:
        pass
