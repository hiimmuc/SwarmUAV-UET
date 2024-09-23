from typing import Dict, Any, Optional, Union
from drone import *


class DroneController:
    def __init__(self, active_drone=None) -> None:
        self.active_drones = active_drone
        self.drones = {}

    def takeOffDrones(self, drones: Dict[str,]) -> None:
        pass

    def connectDrones(self, drones: Dict[str,]) -> None:
        pass

    def armingDrones(self, drones: Dict[str,]) -> None:
        pass

    def returnToLaunchDrones(self, drones: Dict[str,]):
        pass

    def compareDistancesBetweenDrones(self, drones: Dict[str,]):
        pass

    def gotoDrones(self, drones):
        pass
