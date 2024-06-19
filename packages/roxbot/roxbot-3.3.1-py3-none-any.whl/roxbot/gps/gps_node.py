#!/usr/bin/env python3
"""
GPS node listens to mqtt gps topics and aggregates dat

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""
from abc import ABC, abstractmethod
import time

import aiomqtt
import orjson

from roxbot.config import MqttConfig
from roxbot.exceptions import FixException, FixProblem
from roxbot.interfaces import Pose
from roxbot.node import Node


class GpsNodeABC(ABC, Node):
    """abstract base class for creating gps nodes"""

    def __init__(self) -> None:

        super().__init__()

        self.last_update = 0.0  # last update time
        self.x = 0.0  # x position in meters
        self.y = 0.0  # y position in meters
        self.theta = 0.0  # heading in radians (data from gps, not adjusted)
        self.gps_qual = 0  # gps quality

        self._coros.append(self._receive)

    def get_pose(self, max_age: float = 1.0) -> Pose:
        """returns pose or raises FixException if data is too old"""
        if time.time() - self.last_update > max_age:
            raise FixException(FixProblem.OLD_FIX)

        if self.gps_qual != 4:
            raise FixException(FixProblem.NO_RTK_FIX)

        return Pose(self.x, self.y, self.theta)

    @abstractmethod
    async def _receive(self) -> None:
        """receive gps data"""


class GpsNode(GpsNodeABC):
    """interface to gps mqtt data, works in meters and radians.
    latlon conversion is done by the gps sender node"""

    def __init__(self) -> None:  # pylint: disable=useless-super-delegation
        super().__init__()

    async def _receive(self) -> None:
        """receive mqtt messages"""
        cfg = MqttConfig()

        self._log.info(f"Connecting to {cfg.host}:{cfg.port}")
        pos_topic = cfg.gps_position_topic
        dir_topic = cfg.gps_direction_topic

        async with aiomqtt.Client(cfg.host, port=cfg.port) as client:
            await client.subscribe(pos_topic)
            await client.subscribe(dir_topic)
            async for message in client.messages:
                try:
                    data = orjson.loads(message.payload)  # type: ignore
                    self._log.debug(f"received {data=}")
                    if message.topic.matches(pos_topic):
                        self.x = data["x"]
                        self.y = data["y"]
                        self.gps_qual = data["gps_qual"]
                        self.last_update = data["ts"]

                    if message.topic.matches(dir_topic):
                        self.theta = data["theta"]
                        self.last_update = data["ts"]

                except Exception as e:
                    self._log.error(e)
                    self.nr_errors += 1


if __name__ == "__main__":
    # simple standalone demo code
    from roxbot.utils import run_main_async

    gps = GpsNode()
    run_main_async(gps.main())
